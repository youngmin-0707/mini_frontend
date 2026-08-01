"""Google Gemini SDK를 사용해 질문에 대한 답변을 생성합니다.

라우터와 외부 AI API 호출을 분리하면 테스트할 때 Gemini 호출만
가짜 함수로 교체하기 쉽고, 나중에 모델을 바꾸기도 쉽습니다.
"""

import os
from app.schemas.chat_schema import ChatRequest, ChatResponse
from google import genai

def call_gemini(chat_request:ChatRequest)->ChatResponse:
    """환경 변수로 Gemini 클라이언트를 만들고 생성된 답변을 반환합니다."""
    # API 키는 코드에 적지 않고 Render 환경 변수나 .env에서 읽습니다.
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    # 읽은 API 키로 Google Gen AI 서버와 통신할 객체를 만듭니다.
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model = model,
        contents = chat_request.prompt,
    )    
    
    # SDK 응답 전체 중 텍스트만 우리 API의 응답 모델에 담습니다.
    return ChatResponse(
        answer = response.text
    )
