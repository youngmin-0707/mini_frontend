# product_router.py

from fastapi import APIRouter
from app.schemas.auth import (
    AuthLogin, AuthPublic, AuthCreate
)
from app.services.auth_service import (
    sign_up_process, sign_in_process, sign_out_process
)

# 인증 API 주소들을 묶어 관리하는 라우터입니다.
auth_router = APIRouter(tags=["Auth"])

# 회원가입 요청 본문을 AuthCreate 형식으로 검증한 뒤 서비스 함수에 전달합니다.
@auth_router.post("/auth/create")
def create(auth:AuthCreate) -> AuthPublic:
    """신규 입력"""
    return sign_up_process(auth)

# 로그인 요청을 처리하는 POST API입니다.
@auth_router.post("/auth/signin")
def signin(auth:AuthLogin) -> AuthPublic:
    return sign_in_process(auth)

# URL 경로에 포함된 사용자 ID를 받아 로그아웃 서비스를 호출합니다.
@auth_router.get("/auth/signout/{input_id}")
def signout(input_id:str) -> AuthPublic:
    return sign_out_process(input_id)
