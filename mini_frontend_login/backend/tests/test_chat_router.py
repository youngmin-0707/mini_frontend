from fastapi.testclient import TestClient

from app.main import app
from app.schemas.chat_scheme import ChatResponse


client = TestClient(app)


def test_chat_gemini_success(monkeypatch):
    """Gemini API 대신 가짜 함수를 사용해 라우터만 테스트합니다."""

    def fake_call_gemini(chat_request):
        return ChatResponse(answer=f"테스트 답변: {chat_request.prompt}")

    monkeypatch.setattr(
        "app.routers.chat_router.call_gemini",
        fake_call_gemini,
    )

    response = client.post(
        "/chat/gemini",
        json={"user_id": "id01", "prompt": "안녕!"},
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "테스트 답변: 안녕!"}


def test_chat_gemini_rejects_empty_prompt():
    response = client.post(
        "/chat/gemini",
        json={"user_id": "id01", "prompt": ""},
    )

    assert response.status_code == 422


def test_chat_gemini_rejects_missing_user_id():
    response = client.post("/chat/gemini", json={"prompt": "안녕!"})

    assert response.status_code == 422
