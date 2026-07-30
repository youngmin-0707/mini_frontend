"""Customer API에서 사용하는 요청·응답 데이터 모양을 정의합니다."""

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    """고객 등록 화면에서 백엔드로 보내는 데이터입니다."""

    id: str = Field(pattern=r"^id\d{2}$")
    pwd: str = Field(pattern=r"^pwd\d{2}$")
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)


class CustomerUpdate(BaseModel):
    """고객 수정 시 입력받는 데이터입니다. ID와 등록 시각은 바꾸지 않습니다."""

    pwd: str = Field(pattern=r"^pwd\d{2}$")
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)


class CustomerPublic(BaseModel):
    """화면에 보여 줄 고객 데이터입니다. 비밀번호는 포함하지 않습니다."""

    id: str
    name: str
    age: int
    timestamp: str
