"""Supabase `products` 테이블의 CRUD를 담당하는 서비스입니다.

CRUD는 Create(생성), Read(조회), Update(수정), Delete(삭제)의 약자입니다.
각 함수는 Supabase 결과를 `ProductPublic`으로 검증해 라우터에 돌려줍니다.
"""
from app.schemas.product_schema import ProductCreate, ProductPublic, ProductUpdate
from app.core.supabase_client import get_supabase
from zoneinfo import ZoneInfo
from datetime import datetime

# 1. 입력
def product_create(product: ProductCreate) -> ProductPublic | None:
    """새 ID와 등록 시각을 만들어 상품 한 개를 저장합니다."""
    supabase = get_supabase()
    # 서버 위치와 무관하게 한국 시간을 명시적으로 사용합니다.
    now = datetime.now(ZoneInfo("Asia/Seoul"))

    result = (
        supabase.table("products")
         .insert(
            {
                # 년월일시분초와 마이크로초를 이어 붙여 학습용 ID를 만듭니다.
                "id": now.strftime("%Y%m%d%H%M%S%f"),
                "name": product.name,
                "price": product.price,
                "created_at": now.isoformat(),   # timestamptz
            }
        )
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])

# 2. 전체조회
def product_get_all() -> list[ProductPublic]:
    """모든 상품 행을 조회해 Pydantic 모델 목록으로 바꿉니다."""
    supabase = get_supabase()
    result = (
        supabase.table("products")
        .select("*")
        .execute()
    )
    # 리스트 컴프리헨션으로 DB의 각 딕셔너리를 모델로 변환합니다.
    return [ProductPublic.model_validate(item) for item in result.data]

# 3. 한개조회
def product_get(product_id: str) -> ProductPublic | None:
    """`id` 컬럼이 product_id와 같은 상품 한 개를 조회합니다."""
    supabase = get_supabase()

    result = (
        supabase.table("products")
        .select("*")
        .eq("id", product_id)
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])


# 4. 삭제
def product_delete(product_id: str) -> ProductPublic | None:
    """ID가 같은 상품을 삭제하고 삭제된 행을 반환합니다."""
    supabase = get_supabase()
    result = (
        supabase.table("products")
        .delete()
        .eq("id", product_id)
        .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])


# 5. 수정
def product_update(
    product_id: str,
    product: ProductUpdate,
) -> ProductPublic | None:
    """ID가 같은 상품의 이름과 가격을 새 값으로 바꿉니다."""
    supabase = get_supabase()

    result = (
        supabase.table("products")
        .update(
                {
                    "name": product.name,
                    "price": product.price,
                }
            )
            .eq("id", product_id)
            .execute()
    )
    if not result.data:
        return None
    return ProductPublic.model_validate(result.data[0])
