from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import shutil
from pathlib import Path

app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def visualize_and_classify_images(image_path):
    # 테스트를 위한 간단한 구현
    # 실제 도트 이미지 감지 로직은 여기에 구현
    return 1  # 항상 도트 이미지로 판단

def resize_image(image, scale):
    # 테스트를 위한 간단한 리사이즈 구현
    height, width = image.shape[:2]
    new_height = int(height * scale)
    new_width = int(width * scale)
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    return resized

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), scale: float = 2.0):
    # 파일 저장
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 이미지 처리
    image = cv2.imread(str(file_path))
    resized_image = resize_image(image, scale)
    
    # 결과 저장
    output_path = f"resized_{file.filename}"
    cv2.imwrite(str(UPLOAD_DIR / output_path), resized_image)
    
    # 응답 생성
    response_data = {
        "data": {
            "original_size": {
                "width": str(image.shape[1]),
                "height": str(image.shape[0])
            },
            "resized_size": {
                "width": str(resized_image.shape[1]),
                "height": str(resized_image.shape[0])
            }
        },
        "status": {
            "type": "success",
            "message": f"Image processed successfully. Resized file saved as {output_path}."
        }
    }
    return JSONResponse(content=response_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)