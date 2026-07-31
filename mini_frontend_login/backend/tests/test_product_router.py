from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_product_create_success():
    product = {"id": 1, "name": "테스트 상품", "price": 10000}

    response = client.post("/product/create", json=product)

    assert response.status_code == 200
    assert response.json() == product


def test_product_get_one_success():
    response = client.get("/product/get/123")

    assert response.status_code == 200
    assert response.json() == {"id": 123, "name": "크록스", "price": 30000}


def test_product_get_all_success():
    response = client.get("/product/getall")

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0] == {
        "id": 100,
        "name": "pant01",
        "price": 20000,
    }


def test_product_create_rejects_missing_price():
    response = client.post(
        "/product/create",
        json={"id": 1, "name": "테스트 상품"},
    )

    assert response.status_code == 422
