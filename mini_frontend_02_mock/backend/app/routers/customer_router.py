"""Customer 요청을 받아 서비스 함수와 연결하는 API 라우터입니다."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from app.schemes.customer_scheme import (
    CustomerCreate,
    CustomerCreateResponse,
    CustomerDeleteResponse,
    CustomerGetResponse,
    CustomerListResponse,
    CustomerPublic,
    CustomerUpdate,
    CustomerUpdateResponse,
)
from app.services.customer_service import (
    CustomerDuplicateError,
    CustomerNotFoundError,
    CustomerStorageError,
    customer_create,
    customer_delete,
    customer_get,
    customer_get_all,
    customer_update,
)


customer_router = APIRouter(prefix="/customer", tags=["Customer"])

# 주소에 입력하는 ID도 id01 형식인지 검사합니다.
CustomerId = Annotated[str, Path(pattern=r"^id\d{2}$")]


def _public(customer) -> CustomerPublic:
    """저장 데이터에서 비밀번호를 제외한 공개 데이터만 만듭니다."""
    return CustomerPublic.model_validate(customer, from_attributes=True)


def _service_error(error: Exception) -> HTTPException:
    """서비스에서 발생한 오류를 알맞은 HTTP 응답으로 바꿉니다."""
    if isinstance(error, CustomerDuplicateError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="중복된 ID입니다. 다시 입력하세요.",
        )
    if isinstance(error, CustomerNotFoundError):
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
    response_model=CustomerCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(customer: CustomerCreate) -> CustomerCreateResponse:
    try:
        saved = customer_create(customer)
        return CustomerCreateResponse(
            message="등록되었습니다.",
            customer=_public(saved),
        )
    except (CustomerDuplicateError, CustomerStorageError) as error:
        raise _service_error(error)


@customer_router.get("/get/{customer_id}", response_model=CustomerGetResponse)
def get(customer_id: CustomerId) -> CustomerGetResponse:
    try:
        return CustomerGetResponse(customer=_public(customer_get(customer_id)))
    except (CustomerNotFoundError, CustomerStorageError) as error:
        raise _service_error(error)


@customer_router.get("/getall", response_model=CustomerListResponse)
def get_all() -> CustomerListResponse:
    try:
        customers = [_public(customer) for customer in customer_get_all()]
        return CustomerListResponse(count=len(customers), customers=customers)
    except CustomerStorageError as error:
        raise _service_error(error)


@customer_router.put(
    "/update/{customer_id}",
    response_model=CustomerUpdateResponse,
)
def update(customer_id: CustomerId, customer: CustomerUpdate) -> CustomerUpdateResponse:
    try:
        updated = customer_update(customer_id, customer)
        return CustomerUpdateResponse(
            message="수정되었습니다.",
            updated_customer=_public(updated),
        )
    except (CustomerNotFoundError, CustomerStorageError) as error:
        raise _service_error(error)


@customer_router.delete(
    "/delete/{customer_id}",
    response_model=CustomerDeleteResponse,
)
def delete(customer_id: CustomerId) -> CustomerDeleteResponse:
    try:
        deleted_id = customer_delete(customer_id)
        return CustomerDeleteResponse(
            message="삭제되었습니다.",
            deleted_id=deleted_id,
        )
    except (CustomerNotFoundError, CustomerStorageError) as error:
        raise _service_error(error)
