from fastapi import APIRouter, UploadFile, HTTPException
from ..services.image_service import ImageService
from ..utils.file_utils import save_temp_file, remove_temp_file
import cv2

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(image: UploadFile):
    try:
        filepath = await save_temp_file(image)
        if not filepath:
            raise HTTPException(status_code=400, detail="Invalid file type")

        img = cv2.imread(str(filepath), cv2.IMREAD_UNCHANGED)
        if img is None:
            raise HTTPException(status_code=400, detail="Could not read image")

        image_service = ImageService()
        result = image_service.detect_minchunk(img)
        
        remove_temp_file(filepath)
        return result

    except Exception as e:
        if 'filepath' in locals():
            remove_temp_file(filepath)
        raise HTTPException(status_code=500, detail=str(e))