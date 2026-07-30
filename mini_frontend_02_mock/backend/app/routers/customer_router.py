"""Customer 요청을 받아 서비스 함수와 연결하는 API 라우터입니다."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from app.schemes.customer_scheme import (
    CustomerCreate,
    CustomerPublic,
    CustomerUpdate,
)
from app.services.customer_service import (
    customer_create,
    customer_delete,
    customer_get,
    customer_get_all,
    customer_update,
)


customer_router = APIRouter(prefix="/customer", tags=["Customer"])

# 주소에 입력하는 ID도 id01 형식인지 검사합니다.
CustomerId = Annotated[str, Path(pattern=r"^id\d{2}$")]


def _public(customer: dict) -> dict:
    """저장 데이터에서 비밀번호를 제외한 공개 데이터만 만듭니다."""
    return CustomerPublic.model_validate(customer).model_dump()


def _service_error(error: ValueError) -> HTTPException:
    """서비스의 간단한 오류 문구를 HTTP 응답으로 바꿉니다."""
    if str(error) == "duplicate":
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="중복된 ID입니다. 다시 입력하세요.",
        )
    if str(error) == "not_found":
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 Customer가 없습니다.",
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Customer 데이터를 처리하지 못했습니다.",
    )


@customer_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
def create(customer: CustomerCreate) -> dict:
    try:
        saved = customer_create(customer)
        return {
            "message": "등록되었습니다.",
            "customer": _public(saved),
        }
    except ValueError as error:
        raise _service_error(error)


@customer_router.get("/get/{customer_id}")
def get(customer_id: CustomerId) -> dict:
    try:
        return {"customer": _public(customer_get(customer_id))}
    except ValueError as error:
        raise _service_error(error)


@customer_router.get("/getall")
def get_all() -> dict:
    try:
        customers = [_public(customer) for customer in customer_get_all()]
        return {
            "count": len(customers),
            "customers": customers,
        }
    except ValueError as error:
        raise _service_error(error)


@customer_router.put("/update/{customer_id}")
def update(customer_id: CustomerId, customer: CustomerUpdate) -> dict:
    try:
        updated = customer_update(customer_id, customer)
        return {
            "message": "수정되었습니다.",
            "updated_customer": _public(updated),
        }
    except ValueError as error:
        raise _service_error(error)


@customer_router.delete("/delete/{customer_id}")
def delete(customer_id: CustomerId) -> dict:
    try:
        deleted_id = customer_delete(customer_id)
        return {
            "message": "삭제되었습니다.",
            "deleted_id": deleted_id,
        }
    except ValueError as error:
        raise _service_error(error)
