"""회원가입·로그인·로그아웃의 실제 처리 절차를 담은 서비스입니다.

라우터가 검증된 Pydantic 모델을 넘기면 이 파일이 Supabase를
조회하거나 저장합니다. 반환할 때는 비밀번호가 없는 `AuthPublic`을 사용합니다.
"""

from fastapi import HTTPException

from app.core.supabase_client import get_supabase
from app.schemas.auth import AuthCreate, AuthLogin, AuthPublic

def sign_up_process(auth: AuthCreate):
    """중복 ID를 확인한 뒤 새 회원을 customers 테이블에 저장합니다."""
    # DB 작업에 사용할 Supabase 클라이언트를 만듭니다.
    supabase = get_supabase()
    # 같은 ID가 이미 있는지 먼저 조회해 기본 키 충돌을 막습니다.
    db_customer = _customer_get(auth.id)
    if db_customer is not None:
        raise HTTPException(
            status_code=409,
            detail="이미 사용 중인 아이디입니다."
        )
    # Pydantic 모델의 값을 DB 컬럼과 같은 키의 딕셔너리로 바꿔 INSERT합니다.
    result = (
        supabase.table("customers")
         .insert(
            {
                "id": auth.id,
                "pwd": auth.pwd,
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
    # Supabase가 돌려준 첫 번째 행을 안전한 공개용 모델로 변환합니다.
    return AuthPublic.model_validate(result.data[0])


def sign_in_process(auth: AuthLogin):
    """ID로 회원을 찾고 비밀번호가 같은지 검사합니다."""
    db_customer = _customer_get(auth.id)
    if db_customer is None:
        raise HTTPException(
            status_code=404,
            detail="사용자를 찾을 수 없습니다."
        )
    # 학습용 예제라 DB의 문자열과 직접 비교합니다.
    # 실제 서비스에서는 비밀번호 해시 또는 Supabase Auth를 사용해야 합니다.
    if(auth.id == db_customer["id"] and auth.pwd == db_customer["pwd"]):
        payload = {"id": db_customer["id"], "name":db_customer["name"]}
        return AuthPublic.model_validate(payload)
    else:
        raise HTTPException(
            status_code = 401,
            detail = "아이디 또는 패스워드가 올바르지 않습니다."
        )

def sign_out_process(input_id:str):
    """현재는 DB를 변경하지 않고 로그아웃할 ID만 응답합니다."""

    return AuthPublic(
        id = input_id,
    )

def _customer_get(customer_id: str) -> dict | None:
    """customers 테이블에서 ID가 같은 한 행을 찾습니다.

    함수 이름의 밑줄(`_`)은 이 파일 내부에서 쓰는 보조 함수라는 관례입니다.
    결과가 없으면 `None`, 있으면 첫 번째 회원 딕셔너리를 반환합니다.
    """
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
