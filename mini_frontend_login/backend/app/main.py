from fastapi import FastAPI

from app.core import chat_config
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router
from app.routers.auth_router import auth_router


tags_metadata = [
    {
        "name": "Auth",
        "description": "sign up,in ,out"
    },
    {
        "name": "Product",
        "description": "Product 관련 API",
    },
]


app = FastAPI(
    title="Main App",
    openapi_tags=tags_metadata,
)

app.include_router(product_router)
app.include_router(chat_router)
app.include_router(auth_router)