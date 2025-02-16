import os
from typing import Union
from fastapi import UploadFile
from pathlib import Path
from config import settings

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

async def save_temp_file(file: UploadFile) -> Union[str, None]:
    if file and allowed_file(file.filename):
        filepath = os.path.join(settings.UPLOAD_FOLDER, file.filename)
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)
        return filepath
    return None

def remove_temp_file(filepath: str) -> None:
    if os.path.exists(filepath):
        os.remove(filepath)