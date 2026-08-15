from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from app.core.config import get_setting
from app.core.logging import get_logger
from app.utils.redis import get_redis_client, close_redis_client
from app.db.session import engine
from app.api.v1.health import router as health_router
from app.api.v1.router import api_router

setting = get_setting()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("application_starting", environment=setting.ENVIRONMENT)
    get_redis_client()
    
    yield
    
    logger.info("application_shutting_down")
    await close_redis_client()
    await engine.dispose()
    
    

def create_app() -> FastAPI:
    app = FastAPI(
        title=setting.PROJECT_NAME,
        version="1.0.0",
        lifespan=lifespan,
        openapi_tags=[
            {"name": "auth", "description":"Registeration, loging, tokens, google OAuth"},
            {"name": "users", "description": "User resource endpoints."},
            {"name": "health", "description": "Liveness/readiness probes."},
        ]
    )

# --- Middleware (outermost first) -----------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=setting.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=setting.trusted_hosts_list)
# --- Exception handlers ----------------------------------------------
# TODO: add exception handler to this file

# --- Routers -----------------------------------------------------------
    app.include_router(health_router)
    app.include_router(api_router, prefix=setting.API_V1_PREFIX)
    
    app.openapi = lambda: _custom_openapi(app)
    return app

def _custom_openapi(app: FastAPI) -> dict[str, object]:
    if app.openapi_schema:
        return app.openapi_schema
    
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=(
            "Tail API for managing tailoring workshops, clients, orders, measurements, "
            "delivery details, and order progress throughout the tailoring workflow.\n\n"
            "Authenticate via /api/v1/auth/login, then click Authorize and "
            "paste the returned access_token."
        ),
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth":{"type":"http","scheme":"bearer", "bearerFormat":"JWT"}
    }
    
    for path in schema["paths"].values():
        for operation in path.values():
            if operation.get("tags") in (["health"],):
                continue
            if operation.get("operationId", "").startswith(("register", "login", "refresh")):
                continue
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema=schema
    return schema
    
app = create_app()
    