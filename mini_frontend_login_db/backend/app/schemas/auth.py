# auth_scheme.py
from pydantic import BaseModel, Field

# 회원가입할 때 클라이언트가 보내야 하는 데이터 구조입니다.
class AuthCreate(BaseModel):
    id:str
    pwd:str
    name:str


# 로그인할 때 필요한 최소 데이터 구조입니다.
class AuthLogin(BaseModel):
    id:str
    pwd:str
    


# 비밀번호를 제외하고 외부에 공개할 인증 응답 구조입니다.
class AuthPublic(BaseModel):
    id:str
    name:str | None = None
