import cv2
import numpy as np

class ImageService:
    def detect_minchunk(self, image):
        try:
            image_no_bg, mask = self._preprocess_image(image)
            content, _ = self._extract_content(image_no_bg, mask)
            minchunk_info = self._detect_minchunk(content)
            
            if minchunk_info is None:
                return {
                    'data': None,
                    'status': {
                        'type': 'failed',
                        'message': 'Minchunk 탐지에 실패하였습니다.'
                    }
                }
            
            return {
                'data': {
                    'chunksize': str(minchunk_info['chunksize']),
                    'originalsize': {
                        'width': str(minchunk_info['original_dimensions']['width']),
                        'height': str(minchunk_info['original_dimensions']['height'])
                    },
                    'minchunksize': {
                        'width': str(minchunk_info['minchunk_dimensions']['width']),
                        'height': str(minchunk_info['minchunk_dimensions']['height'])
                    }
                },
                'status': {
                    'type': 'success',
                    'message': 'Minchunk가 탐지되었습니다.'
                }
            }
        except Exception as e:
            return {
                'data': None,
                'status': {
                    'type': 'failed',
                    'message': 'Minchunk 탐지에 실패하였습니다.'
                }
            }

    def _preprocess_image(self, image):
        if image.shape[2] == 4:
            alpha_channel = image[:, :, 3]
            if np.all(alpha_channel == 255):
                image_no_bg = image[:, :, :3]
                gray = cv2.cvtColor(image_no_bg, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            else:
                _, mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)
                image_no_bg = image[:, :, :3]
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            image_no_bg = image
        return image_no_bg, mask

    def _extract_content(self, image, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])
        content = image[y:y+h, x:x+w]
        return content, (x, y, w, h)

    def _detect_minchunk(self, content):
        height, width = content.shape[:2]
        min_val = min(height, width)
        
        common_divisors = [i for i in range(1, min_val + 1) 
                         if height % i == 0 and width % i == 0]

        for element in reversed(common_divisors):
            if element == 1:
                return None
                
            new_height = int(height / element)
            new_width = int(width / element)
            
            minchunk_image = cv2.resize(content, (new_width, new_height), 
                                      interpolation=cv2.INTER_NEAREST)
            restored = cv2.resize(minchunk_image, (width, height), 
                                interpolation=cv2.INTER_NEAREST)
            
            if self._compare_images(content, restored):
                return {
                    'chunksize': element,
                    'original_dimensions': {
                        'width': width,
                        'height': height
                    },
                    'minchunk_dimensions': {
                        'width': new_width,
                        'height': new_height
                    }
                }
        return None

    def _compare_images(self, image1, image2):
        difference = cv2.absdiff(image1, image2)
        _, diff = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
        return np.count_nonzero(diff) == 0