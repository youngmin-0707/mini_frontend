from app.core.supabase_client import get_supabase
from fastapi import HTTPException
from app.schemas.auth_scheme import (
    AuthCreate, AuthLogin, AuthPublic,AuthPasswordUpdate
)
from app.core.password import hash_password, verify_password

def sign_up_process(auth: AuthCreate):
    """ 회원 가입 """
    supabase = get_supabase()
    if  _customer_get(auth.id):
        raise HTTPException(
            status_code=409,
            detail="이미 사용 중인 아이디입니다."
        )
    result = (
        supabase.table("customers")
         .insert(
            {
                "id": auth.id,
                "pwd": hash_password(auth.pwd),
                "name": auth.name,
            }
        )
        .execute()
    )
    if not result.data:
        raise HTTPException(
                status_code = 500,
                detail = "DB 장애"
            )
    return AuthPublic.model_validate(result.data[0])


def sign_in_process(auth: AuthLogin):
    """ 회원 로그인 """
    db_customer = _customer_get(auth.id)
    if db_customer is None:
        raise HTTPException(
            status_code= 401,
            detail="사용자를 찾을 수 없습니다."
        )
    if verify_password(auth.pwd, db_customer["pwd"]):
        return AuthPublic.model_validate(db_customer)
    else:
        raise HTTPException(
            status_code = 401,
            detail = "아이디 또는 패스워드가 올바르지 않습니다."
        )

def sign_out_process(input_id:str):
    """ 회원 로그 아웃 """

    return AuthPublic(
        id = input_id,
    )

def get_auth_process(input_id:str):
    """ 회원 정보 조회 """
    db_customer = _customer_get(input_id)

    if db_customer is None:
        raise HTTPException(
            status_code=401
            ,
            detail="사용자를 찾을 수 없습니다."
        )

    return AuthPublic.model_validate(db_customer)


def update_password_process(auth: AuthPasswordUpdate):
    """ 회원 비밀번호 변경 """
    db_customer = _customer_get(auth.id)

    if db_customer is None or not verify_password(auth.current_pwd, db_customer["pwd"]):
        raise HTTPException(
            status_code=404,
            detail="아이디 또는 현재 비밀번호가 올바르지 않습니다."
        )

    (
        get_supabase()
        .table("customers")
        .update({"pwd": hash_password(auth.new_pwd)})
        .eq("id", auth.id)
        .execute()
    )

    return AuthPublic.model_validate(db_customer)


def _customer_get(customer_id: str) -> dict | None:
    supabase = get_supabase()

    result = (
        supabase.table("customers")
        .select("*")
        .eq("id", customer_id)
        .execute()
    )
    if not result.data:
        return None
    return result.data[0]
