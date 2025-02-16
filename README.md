# MinChunk Image Analysis API

이미지의 MinChunk를 탐지하고 분석하는 FastAPI 기반의 API 서버입니다.

## 프로젝트 구조

```
project/
│
├── app/
│   ├── __init__.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── image_router.py    # API 엔드포인트 정의
│   ├── services/
│   │   ├── __init__.py
│   │   └── image_service.py   # MinChunk 분석 로직
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py      # 파일 처리 유틸리티
│
├── config.py                  # 설정 관리
└── main.py                   # 애플리케이션 진입점
└── test_request.py            # 예시 이미지 Request로 테스트
```

## 기능

- 이미지 업로드 및 MinChunk 분석
- 로컬 네트워크 내 API 공유
- 비동기 파일 처리
- 자동 임시 파일 관리

## API 명세

### 이미지 분석 엔드포인트

- URL: `/api/analyze-image`
- Method: `POST`
- Content-Type: `multipart/form-data`

#### Request

```
{
    (이미지 파일만 포함)
}
```

#### Response

```json
{
  "data": {
    "chunksize": "3",
    "originalsize": {
      "width": "12",
      "height": "12"
    },
    "minchunksize": {
      "width": "4",
      "height": "4"
    }
  },
  "status": {
    "type": "success|failed",
    "message": "Minchunk가 탐지되었습니다.|Minchunk 탐지에 실패하였습니다."
  }
}
```

## 설치 및 실행

### 요구사항

```bash
pip install fastapi uvicorn python-multipart opencv-python
```

### 실행 방법

```bash
python main.py
```

서버가 시작되면 로컬 IP 주소와 함께 다음 정보가 표시됩니다:

- API 서버 IP
- API 문서 URL (Swagger UI)
- API 엔드포인트 URL

## 로컬 네트워크 공유

- 같은 와이파이 네트워크의 모든 기기에서 API 접근 가능
- `http://{서버IP}:8000/docs`에서 API 문서 확인 및 테스트 가능

## 주요 구성 요소

### 이미지 처리 서비스 (`image_service.py`)

- 이미지 전처리
- MinChunk 크기 감지
- 결과 포맷팅

### 파일 관리 (`file_utils.py`)

- 파일 확장자 검증
- 임시 파일 저장 및 삭제
- 파일 경로 관리

### 설정 관리 (`config.py`)

- 업로드 폴더 설정
- 허용 파일 형식 정의
- 파일 크기 제한 설정

## 보안 고려사항

- 개발 환경용으로 설계됨
- 프로덕션 환경에서는 추가 보안 설정 필요
- 허용된 파일 형식만 처리

## 참고사항

- FastAPI의 비동기 처리 활용
- OpenCV 기반 이미지 처리
- 자동 API 문서화 지원
- 효율적인 리소스 관리
