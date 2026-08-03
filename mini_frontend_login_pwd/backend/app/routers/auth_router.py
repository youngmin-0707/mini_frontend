# product_router.py

from fastapi import APIRouter
from app.schemas.auth_scheme import (
    AuthLogin, AuthPublic, AuthCreate, AuthPasswordUpdate
)
from app.services.auth_service import (
    sign_up_process,
    sign_in_process,
    sign_out_process,
    get_auth_process,
    update_password_process,
)

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/auth/create")
def create(auth:AuthCreate) -> AuthPublic:
    """신규 입력"""
    return sign_up_process(auth)

@auth_router.post("/auth/signin")
def signin(auth:AuthLogin) -> AuthPublic:
    return sign_in_process(auth)


@auth_router.get("/auth/get")
def get_auth(id:str) -> AuthPublic:
    """ ID를 입력하면 회원 ID와 이름 반환 """
    return get_auth_process(id)


@auth_router.put("/auth/password")
def update_password(auth:AuthPasswordUpdate) -> AuthPublic:
    """ 현재 비밀번호 확인 후 새 비밀번호로 변경 """
    return update_password_process(auth)

@auth_router.get("/auth/signout/{input_id}")
def signout(input_id:str) -> AuthPublic:
    return sign_out_process(input_id)
