from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.database import Base, engine
from app.middleware.jwt_middleware import JwtMiddleware
from app.routers import order_reports, product_reports


# Tao bang trong DB rieng
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bài thực hành 5 - Reporting Service",
    description="Dịch vụ báo cáo (SOA) - xác thực qua JWT của Auth Service (TH2)"
)


# Them Middleware JWT
app.add_middleware(JwtMiddleware)


# Dang ky router
app.include_router(order_reports.router)
app.include_router(product_reports.router)


@app.get("/", tags=["Health"])
def home():
    return {"message": "Reporting Service (TH5) đang chạy"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
