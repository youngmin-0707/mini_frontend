# product_router.py

from fastapi import APIRouter
from app.schemas.auth import (
    AuthLogin, AuthPublic, AuthCreate
)
from app.services.auth_service import (
    sign_up_process, sign_in_process, sign_out_process
)

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/auth/create")
def create(auth:AuthCreate) -> AuthPublic:
    """신규 입력"""
    return sign_up_process(auth)

@auth_router.post("/auth/signin")
def signin(auth:AuthLogin) -> AuthPublic:
    return sign_in_process(auth)

@auth_router.get("/auth/signout/{input_id}")
def signout(input_id:str) -> AuthPublic:
    return sign_out_process(input_id)
