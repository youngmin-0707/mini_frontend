"""상품 API의 입력·수정·출력 데이터 모양을 정의합니다.

동일한 상품이라도 생성할 때는 이름과 가격만 받고,
응답할 때는 DB가 만든 ID와 등록 시각까지 포함하므로 모델을 나누었습니다.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """상품 등록 요청 모델입니다."""
    name: str = Field(min_length=1, max_length=50, examples=["바지"])
    price: int = Field(ge=1, examples=[10000])


class ProductUpdate(BaseModel):
    """상품 수정 요청 모델입니다."""
    name: str = Field(min_length=1, max_length=50, examples=["청바지"])
    price: int = Field(ge=1, examples=[20000])


class ProductPublic(BaseModel):
    """DB 조회 결과를 클라이언트에 공개할 때 사용하는 모델입니다."""
    id: str = Field(examples=["20260721170435315246"])
    name: str
    price: int
    created_at: datetime
