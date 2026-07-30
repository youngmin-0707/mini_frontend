"""Customer 화면에서 사용하는 백엔드 API 호출 함수입니다."""

from core.api_client import request


def customer_insert(customer: dict):
    """새 고객을 등록합니다."""
    return request("POST", "/customer/create", json=customer)


def customer_select(customer_id: str):
    """ID로 고객 한 명을 조회합니다."""
    return request("GET", f"/customer/get/{customer_id}")


def customer_select_all():
    """등록된 모든 고객을 조회합니다."""
    return request("GET", "/customer/getall")
