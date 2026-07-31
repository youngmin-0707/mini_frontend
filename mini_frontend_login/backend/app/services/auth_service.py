from fastapi import HTTPException
from app.schemas.auth import (
    AuthCreate, AuthLogin, AuthPublic)

def sign_in_process(auth:AuthCreate):
    """ 회원가입"""
    return AuthPublic(
        id = auth.id,
        name = "이말숙"
    )    

def sign_out_process(input_id: str):

    """ 회원 로그인"""
    if(auth.id == "id01" and auth.pwd == "pwd01"):
        return AuthPublic(
            id = auth.id,
            name = "이말숙"
        )
    else:
        raise HTTPException(
            status_code= 401,
            detail= "아이디 또는 패스워드가 올바르지 않습니다."
            

        )

def sign_up_process(auth: AuthCreate):
    return AuthPublic(
        id=auth.id,
        name=auth.name,
    )
