"""챗 라우터의 정상 응답과 입력 검증을 확인하는 테스트입니다.

실제 Gemini API를 호출하면 테스트가 느리고 API 비용이 들 수 있습니다.
그래서 monkeypatch로 `call_gemini`를 즉시 답하는 가짜 함수로 교체합니다.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat_router
from app.schemas.chat_schema import ChatResponse


# 실제 서버를 띄우지 않고 FastAPI 앱에 HTTP 요청을 보낼 테스트 클라이언트입니다.
client = TestClient(app)


def test_chat_gemini_returns_chat_response(monkeypatch):
    """정상 질문이 200과 예상한 답변을 반환하는지 검사합니다."""
    monkeypatch.setattr(
        chat_router,
        "call_gemini",
        lambda chat_request: ChatResponse(answer=f"응답: {chat_request.prompt}"),
    )

    response = client.post(
        "/chat/gemini",
        json={"user_id": "user-1", "prompt": "안녕"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["answer"] == "응답: 안녕"


def test_chat_gemini_rejects_empty_prompt():
    """빈 질문을 Pydantic이 422로 거절하는지 검사합니다."""
    response = client.post(
        "/chat/gemini",
        json={"user_id": "user-1", "prompt": ""},
    )

    assert response.status_code == 422
