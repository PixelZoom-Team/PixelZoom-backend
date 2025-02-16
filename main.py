from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import image_router
import socket

app = FastAPI()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    local_ip = get_local_ip()
    print(f"\n=== 로컬 네트워크 API 서버 ===")
    print(f"서버 IP: {local_ip}")
    print(f"API 문서: http://{local_ip}:8000/docs")
    print(f"API 엔드포인트: http://{local_ip}:8000/api/analyze-image")
    print("==============================\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)