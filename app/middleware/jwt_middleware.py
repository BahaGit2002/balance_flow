from fastapi.responses import JSONResponse

from app.config.security import decode_jwt


async def jwt_middleware(request, call_next):
    if (request.url.path.startswith(
            "/auth"
    ) or request.url.path.startswith(
        "/docs"
    ) or request.url.path.startswith("/openapi.json")):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401, content={"detail": "Missing token"}
        )

    token = auth_header.split(" ")[1]
    try:
        request.state.user = decode_jwt(token)
    except Exception:
        return JSONResponse(
            status_code=401, content={"detail": "Invalid token"}
        )
    return await call_next(request)
