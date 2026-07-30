# product_client.py
# product CRUD

from typing import Any
from core.api_client import request


def product_insert(product: dict):
    return request("POST", f"/product/create",json = product)
    

def product_delete(product_id: int):
    return request("DELETE", f"/product/delete/{product_id}")


def product_update(product_id : int, product : dict):
    return request("PUT", f"/product/update/{product_id}",json = product)


def product_select_all():
    return request("GET", "/product/getall")


def product_select(product_id: int):
    return request("GET", f"/product/get/{product_id}")