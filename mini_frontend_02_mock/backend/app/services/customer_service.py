"""JSON 파일을 이용해 Customer 데이터를 등록·조회·수정·삭제합니다."""

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app.schemes.customer_scheme import CustomerCreate, CustomerStored, CustomerUpdate


# 이 경로만 바꾸면 다른 JSON 파일을 사용할 수 있습니다.
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "customers.json"


class CustomerNotFoundError(Exception):
    """요청한 고객 ID가 없을 때 사용하는 오류입니다."""


class CustomerDuplicateError(Exception):
    """이미 등록된 고객 ID를 다시 등록할 때 사용하는 오류입니다."""


class CustomerStorageError(Exception):
    """JSON 파일을 읽거나 저장하지 못했을 때 사용하는 오류입니다."""


def _read_customers() -> list[CustomerStored]:
    """JSON 파일의 내용을 Customer 객체 목록으로 바꿉니다."""
    if not DATA_FILE.exists():
        return []

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError
        return [CustomerStored.model_validate(customer) for customer in data]
    except (OSError, ValueError, json.JSONDecodeError):
        raise CustomerStorageError from None


def _write_customers(customers: list[CustomerStored]) -> None:
    """Customer 객체 목록을 한글이 깨지지 않는 JSON 파일로 저장합니다."""
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = [customer.model_dump() for customer in customers]
        DATA_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        raise CustomerStorageError from None


def customer_create(customer: CustomerCreate) -> CustomerStored:
    customers = _read_customers()

    if any(saved.id == customer.id for saved in customers):
        raise CustomerDuplicateError

    # 사용자가 입력하지 않는 등록 시각은 서버에서 자동으로 만듭니다.
    new_customer = CustomerStored(
        **customer.model_dump(),
        timestamp=datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds"),
    )
    customers.append(new_customer)
    _write_customers(customers)
    return new_customer


def customer_get(customer_id: str) -> CustomerStored:
    for customer in _read_customers():
        if customer.id == customer_id:
            return customer
    raise CustomerNotFoundError


def customer_get_all() -> list[CustomerStored]:
    return _read_customers()


def customer_update(customer_id: str, update: CustomerUpdate) -> CustomerStored:
    customers = _read_customers()

    for index, saved in enumerate(customers):
        if saved.id == customer_id:
            # 기존 ID와 최초 등록 시각은 유지하고 입력 항목만 변경합니다.
            updated = CustomerStored(
                id=saved.id,
                timestamp=saved.timestamp,
                **update.model_dump(),
            )
            customers[index] = updated
            _write_customers(customers)
            return updated

    raise CustomerNotFoundError


def customer_delete(customer_id: str) -> str:
    customers = _read_customers()

    for index, saved in enumerate(customers):
        if saved.id == customer_id:
            customers.pop(index)
            _write_customers(customers)
            return customer_id

    raise CustomerNotFoundError
