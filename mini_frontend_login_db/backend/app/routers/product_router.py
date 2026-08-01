"""상품 CRUD HTTP API를 정의하는 라우터입니다.

처리 흐름은 `프론트엔드 → 라우터 → 서비스 → Supabase`입니다.
라우터는 요청과 응답에 집중하고 DB 작업은 `product_service.py`에 맡깁니다.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.product_service import (
    product_create,
    product_delete,
    product_get,
    product_get_all,
    product_update,
)
from app.core.api_response import ApiResponse

product_router = APIRouter(tags=["Product"])

# 200: 정상 - 정상 실행 되면 자동 전송
# 400: 잘못된 요청
# 401: 로그인 필요
# 403: 권한 없음
# 404: 데이터 없음
# 409: 중복 데이터
# 422: 입력값 검증 실패
# 500: 서버 또는 DB 처리 실패

# 1. create
@product_router.post("/product/create")
def create(product: ProductCreate) -> ApiResponse:
    """검증된 상품 정보를 저장하고 생성된 상품을 반환합니다."""
    created_product = product_create(product)
    if created_product is None:
        raise HTTPException(
            status_code=500,
            detail="상품 등록에 실패했습니다.",
        )
    response = ApiResponse(
        success = True,
        message="상품이 등록되었습니다.",
        data = created_product
    )
    return response

# 2. 한개 조회
@product_router.get("/product/get/{product_id}")
def get(product_id: str) -> ApiResponse:
    """URL에서 받은 상품 ID로 상품 한 개를 조회합니다."""

    product = product_get(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"상품 ID {product_id}를 찾을 수 없습니다."
        )
    response = ApiResponse(
        success = True,
        message="상품 조회에 성공했습니다.",
        data = product
    )
    return response

# 3. 전체 조회
@product_router.get("/product/getall")
def get_all() -> ApiResponse:
    """Supabase에 저장된 모든 상품을 목록으로 반환합니다."""
    products = product_get_all()
    response = ApiResponse(
        success = True,
        message="상품 목록 조회에 성공했습니다.",
        data = products
    )
    return response

# 4. 한개 삭제
@product_router.delete("/product/delete/{product_id}")
def delete(product_id: str) -> ApiResponse:
    """상품 ID와 일치하는 행을 삭제합니다."""
    product = product_delete(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"상품 ID {product_id}를 찾을 수 없습니다."
        )
    response = ApiResponse(
        success = True,
        message="상품이 삭제되었습니다.",
        data = product
    )
    return response

# 5. 수정
@product_router.put("/product/{product_id}")
def update(product_id: str, product: ProductUpdate) -> ApiResponse:
    """상품 ID를 찾아 이름과 가격을 수정합니다."""
    updated_product = product_update(product_id, product)
    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail=f"상품 ID {product_id}를 찾을 수 없습니다."
        )
    response = ApiResponse(
        success = True,
        message="상품이 수정되었습니다.",
        data = updated_product
    )
    return response
