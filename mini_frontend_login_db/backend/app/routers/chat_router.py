"""Gemini 챗 API의 URL과 응답 형식을 정의하는 라우터입니다.

요청은 `ChatRequest`로 검증하고, 실제 Gemini 호출은
`chat_service.call_gemini()`에 위임한 뒤 공통 `ApiResponse`로 감싸 반환합니다.
"""

from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import call_gemini
from app.core.api_response import ApiResponse

# `tags`는 Swagger 문서에서 이 API를 Chat 그룹으로 묶습니다.
chat_router = APIRouter(tags=["Chat"])

@chat_router.post("/chat/gemini")
def chat_gemini(chat_request:ChatRequest) -> ApiResponse:
    """사용자 질문을 Gemini에 전달하고 표준 JSON 응답을 만듭니다."""
    # 학습 중 요청 값이 잘 들어오는지 Render/Uvicorn 로그에서 확인합니다.
    print(chat_request.user_id)
    print(chat_request.prompt)
    # Gemini의 ChatResponse를 data 필드에 넣어 공통 응답을 만듭니다.
    response = ApiResponse(
        success = True,
        message = f"정상 !",
        data = call_gemini(chat_request)
    )
    return response
