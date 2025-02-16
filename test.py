import cv2
import numpy as np
import sys

def analyze_minchunk(image_path):
    # 이미지 로드
    try:
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError("이미지를 불러올 수 없습니다.")
    except Exception as e:
        print(f"이미지 로드 에러: {str(e)}")
        return None

    # 이미지 전처리
    try:
        if image.shape[2] == 4:  # 알파 채널이 있는 경우
            alpha_channel = image[:, :, 3]
            if np.all(alpha_channel == 255):
                image_no_bg = image[:, :, :3]
                gray = cv2.cvtColor(image_no_bg, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            else:
                _, mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)
                image_no_bg = image[:, :, :3]
        else:  # RGB 이미지
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            image_no_bg = image

        # 내용물 추출
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])
        content = image_no_bg[y:y+h, x:x+w]

        # MinChunk 분석
        height, width = content.shape[:2]
        min_val = min(height, width)
        
        # 공약수 찾기
        common_divisors = []
        for i in range(1, min_val + 1):
            if height % i == 0 and width % i == 0:
                common_divisors.append(i)

        # MinChunk 검출
        for element in reversed(common_divisors):
            new_height = int(height / element)
            new_width = int(width / element)
            
            minchunk_image = cv2.resize(content, (new_width, new_height), 
                                      interpolation=cv2.INTER_NEAREST)
            restored = cv2.resize(minchunk_image, (width, height), 
                                interpolation=cv2.INTER_NEAREST)
            
            # 이미지 비교
            difference = cv2.absdiff(content, restored)
            _, diff = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
            if np.count_nonzero(diff) == 0 and element != 1:
                return {
                    'minchunk_size': element,
                    'original_size': (width, height),
                    'minchunk_dimensions': (new_width, new_height)
                }

        return None

    except Exception as e:
        print(f"분석 중 에러 발생: {str(e)}")
        return None

def main():
    if len(sys.argv) != 2:
        print("사용법: python script.py <이미지_경로>")
        return

    image_path = sys.argv[1]
    result = analyze_minchunk(image_path)

    if result:
        print("\n=== MinChunk 분석 결과 ===")
        print(f"MinChunk 크기: {result['minchunk_size']}")
        print(f"원본 크기: {result['original_size'][0]}x{result['original_size'][1]}")
        print(f"MinChunk 차원: {result['minchunk_dimensions'][0]}x{result['minchunk_dimensions'][1]}")
    else:
        print("이미지가 이미 MinChunk이거나 분석에 실패했습니다.")

if __name__ == "__main__":
    main()