"""Gemini 챗 API의 요청과 응답 데이터 규칙을 정의합니다."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """누가 무엇을 물었는지 표현하는 요청 모델입니다."""
    # min_length=1은 빈 문자열을 막고, examples는 Swagger 예시를 만듭니다.
    user_id: str = Field(min_length=1, examples=["id01"])
    prompt: str = Field(min_length=1, examples=["안녕!"])


class ChatResponse(BaseModel):
    """Gemini가 생성한 답변을 담는 응답 모델입니다."""
    answer: str = Field(min_length=1, examples=["안녕하세요!"])
