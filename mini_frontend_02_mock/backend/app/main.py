from fastapi import FastAPI
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router
import app.core.chat_config  

tags_metadata = [
    {
        "name":"Chat",
        "description":"Gemini 연동"
    },
    {
        "name":"Product",
        "description":"Product 연동"        
    },
]

app = FastAPI(title="Main App", openapi_tags=tags_metadata)

app.include_router(chat_router)
app.include_router(product_router)

