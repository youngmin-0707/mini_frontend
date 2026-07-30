# product_service.py
from app.schemes.product_scheme import ProductPublic
from zoneinfo import ZoneInfo
from datetime import datetime

# 1. 입력
def product_create(product: ProductPublic) -> ProductPublic | None:
    # Database 에 입력
    return ProductPublic(
        id = product.id,
        name = product.name,
        price = product.price
    )

# 2. 전체조회
def product_get_all() -> list[ProductPublic]:
    list = []
    list.append(ProductPublic(
        id = 100,
        name = "바지",
        price = 20000
    ))
    list.append(ProductPublic(
        id = 101,
        name = "바지",
        price = 30000
    ))
    list.append(ProductPublic(
        id = 103,
        name = "바지",
        price = 40000
    ))
    list.append(ProductPublic(
        id = 104,
        name = "바지",
        price = 50000
    ))
    return list 

# 3. 한개조회
def product_get(product_id: str) -> ProductPublic | None:

    return ProductPublic(
        id = product_id,
        name = "바지",
        price = 20000
    )

# 4. 삭제
def product_delete(product_id: int) -> ProductPublic | None:

    return ProductPublic(
        id = product_id,
        name = "삭제된바지",
        price = 20000
    )
# 5. 수정
def product_update(product_id, product: ProductPublic) -> ProductPublic | None:

    return ProductPublic(
        id = product_id,
        name = "수정된바지",
        price = 20000
    )