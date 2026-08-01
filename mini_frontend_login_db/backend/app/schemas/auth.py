"""인증 API에서 주고받는 데이터의 모양을 정의합니다.

FastAPI는 요청 JSON을 이 Pydantic 모델로 검증합니다.
필수 필드가 빠지거나 타입이 맞지 않으면 라우터 실행 전에 422를 반환합니다.
"""
from pydantic import BaseModel, Field

# 회원가입할 때 클라이언트가 보내야 하는 데이터 구조입니다.
class AuthCreate(BaseModel):
    """회원가입 요청에 필요한 전체 정보입니다."""
    id:str
    pwd:str
    name:str


# 로그인할 때 필요한 최소 데이터 구조입니다.
class AuthLogin(BaseModel):
    """로그인 확인에 필요한 ID와 비밀번호입니다."""
    id:str
    pwd:str
    


# 비밀번호를 제외하고 외부에 공개할 인증 응답 구조입니다.
class AuthPublic(BaseModel):
    """응답용 모델으로, 보안을 위해 비밀번호를 포함하지 않습니다."""
    id:str
    name:str | None = None
