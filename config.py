from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    UPLOAD_FOLDER: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_uploads')
    ALLOWED_EXTENSIONS: set = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024

    class Config:
        case_sensitive = True

settings = Settings()
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)