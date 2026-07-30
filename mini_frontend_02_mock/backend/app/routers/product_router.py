# product_router.py

from fastapi import APIRouter
from app.schemes.product_scheme import ProductPublic, ProductUpdate
from app.services.product_service import (
    product_get_all,
    product_get,
    product_create,
    product_delete,
    product_update,
)

product_router = APIRouter(tags=["Product"])

@product_router.post("/product/create")
def create(product:ProductPublic) -> ProductPublic:
    """Product 신규 입력"""
    return product_create(product)

@product_router.get("/product/get/{product_id}")
def get(product_id:int) -> ProductPublic:
    return product_get(product_id)

@product_router.get("/product/getall")
def get_all() -> list[ProductPublic]:
    return product_get_all()

@product_router.delete("/product/delete/{product_id}")
def delete(product_id: int) -> ProductPublic:
    return product_delete(product_id)

@product_router.put("/product/update/{product_id}")
def update(product_id: int, product: ProductUpdate) -> ProductPublic:
    return product_update(product_id, product)