"""Customer API가 JSON 파일을 사용해 정상 동작하는지 확인합니다."""

import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import customer_service


client = TestClient(app)


@pytest.fixture(autouse=True)
def use_temporary_customer_file(tmp_path, monkeypatch):
    """테스트가 실제 customers.json을 변경하지 않도록 임시 파일을 사용합니다."""
    data_file = tmp_path / "customers.json"
    data_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(customer_service, "DATA_FILE", data_file)


def _customer_payload(customer_id: str = "id01") -> dict:
    return {
        "id": customer_id,
        "pwd": "pwd01",
        "name": "홍길동",
        "age": 25,
    }


def test_customer_create_saves_json_without_exposing_password():
    response = client.post("/customer/create", json=_customer_payload())

    assert response.status_code == 201
    assert response.json()["message"] == "등록되었습니다."
    assert response.json()["customer"]["id"] == "id01"
    assert "pwd" not in response.json()["customer"]

    saved = json.loads(customer_service.DATA_FILE.read_text(encoding="utf-8"))
    assert saved[0]["pwd"] == "pwd01"
    assert saved[0]["timestamp"]


def test_customer_create_rejects_duplicate_id():
    client.post("/customer/create", json=_customer_payload())
    response = client.post("/customer/create", json=_customer_payload())

    assert response.status_code == 409
    assert response.json() == {
        "detail": "중복된 ID입니다. 다시 입력하세요."
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", "user01"),
        ("pwd", "password"),
        ("name", ""),
        ("age", 151),
    ],
)
def test_customer_create_rejects_wrong_input(field, value):
    payload = _customer_payload()
    payload[field] = value

    response = client.post("/customer/create", json=payload)

    assert response.status_code == 422
    assert response.json() == {"detail": "잘못 기입하셨습니다."}


def test_customer_get_one_and_get_all():
    client.post("/customer/create", json=_customer_payload("id01"))
    client.post("/customer/create", json=_customer_payload("id02"))

    one_response = client.get("/customer/get/id01")
    all_response = client.get("/customer/getall")

    assert one_response.status_code == 200
    assert one_response.json()["customer"]["id"] == "id01"
    assert "pwd" not in one_response.json()["customer"]
    assert all_response.status_code == 200
    assert all_response.json()["count"] == 2
    assert len(all_response.json()["customers"]) == 2


def test_customer_update_keeps_original_timestamp():
    created = client.post("/customer/create", json=_customer_payload()).json()
    timestamp = created["customer"]["timestamp"]

    response = client.put(
        "/customer/update/id01",
        json={"pwd": "pwd02", "name": "김영희", "age": 30},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "수정되었습니다."
    assert response.json()["updated_customer"]["name"] == "김영희"
    assert response.json()["updated_customer"]["timestamp"] == timestamp
    assert "pwd" not in response.json()["updated_customer"]


def test_customer_delete_removes_customer():
    client.post("/customer/create", json=_customer_payload())

    delete_response = client.delete("/customer/delete/id01")
    get_response = client.get("/customer/get/id01")

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "삭제되었습니다.",
        "deleted_id": "id01",
    }
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "해당 Customer가 없습니다."}


def test_missing_customer_returns_404():
    response = client.get("/customer/get/id99")

    assert response.status_code == 404
    assert response.json() == {"detail": "해당 Customer가 없습니다."}
