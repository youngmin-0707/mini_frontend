"""FastAPI 백엔드의 시작점입니다.

실행 흐름:
1. 환경 변수를 로드합니다.
2. FastAPI 앱 객체를 만듭니다.
3. 챗·상품·인증 라우터를 앱에 연결합니다.
4. Uvicorn이 `app` 객체를 읽어 HTTP 요청을 받습니다.
"""

from fastapi import FastAPI
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router
from app.routers.auth_router import auth_router
import app.core.chat_config  

# Swagger `/docs`에서 API를 기능별로 보여 줄 설명입니다.
tags_metadata = [
    {
        "name": "Auth",
        "description": "sign up,in,out",
    },
    {
        "name": "Chat",
        "description": "Gemini 모델을 사용해 사용자 메시지에 답변합니다.",
    },
    {
        "name": "Product",
        "description": "Supabase에 저장된 상품을 생성·조회·수정·삭제합니다.",
    },
]

# 서버 전체를 대표하는 FastAPI 앱을 한 번만 생성합니다.
app = FastAPI(title="Main App",openapi_tags=tags_metadata)

# 각 라우터에 정의된 URL을 메인 앱에 등록합니다.
app.include_router(chat_router)
app.include_router(product_router)
app.include_router(auth_router)
