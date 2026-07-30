from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers.chat_router import chat_router
from app.routers.customer_router import customer_router
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
    {
        "name":"Customer",
        "description":"Customer JSON CRUD 연동"
    },
]

app = FastAPI(title="Main App", openapi_tags=tags_metadata)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, error: RequestValidationError):
    """Customer 입력 오류는 초보자도 이해하기 쉬운 한글 메시지로 반환합니다."""
    if request.url.path.startswith("/customer/"):
        return JSONResponse(
            status_code=422,
            content={"detail": "잘못 기입하셨습니다."},
        )

    # 기존 API는 FastAPI의 기본 검증 오류 형식을 그대로 유지합니다.
    return JSONResponse(status_code=422, content={"detail": error.errors()})


app.include_router(chat_router)
app.include_router(product_router)
app.include_router(customer_router)

