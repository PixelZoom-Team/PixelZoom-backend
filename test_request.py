import requests
import json

def test_image_analysis(image_path):
    url = 'http://localhost:8000/api/analyze-image'
    
    # 이미지 파일 열기
    files = {
        'image': open(image_path, 'rb')
    }
    
    try:
        # API 요청
        response = requests.post(url, files=files)
        
        # 응답 출력
        print("\n=== API 테스트 결과 ===")
        print("Status Code:", response.status_code)
        print("\nResponse:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # 파일 닫기
        files['image'].close()

if __name__ == "__main__":
    # 테스트할 이미지 경로
    test_image = "test_img.png"  # 테스트 이미지 파일명
    test_image_analysis(test_image)