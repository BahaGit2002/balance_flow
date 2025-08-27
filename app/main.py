from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router
from app.api.routes.admin import router as admin_router
from app.api.routes.webhook import router as webhook_router
from app.middleware.jwt_middleware import jwt_middleware
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


app.middleware("http")(jwt_middleware)
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(webhook_router, prefix="/webhook", tags=["webhook"])
