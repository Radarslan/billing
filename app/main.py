import logging

import uvicorn  # type: ignore
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.settings.settings import settings


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, openapi_url="/api/v1/openapi.json"
    )

    init_middlewares(application)

    application.include_router(api_router, prefix=settings.API_VERSION)
    return application


def init_middlewares(application: FastAPI) -> None:
    origins = []
    if settings.BACKEND_CORS_ORIGINS:
        origins_raw = settings.BACKEND_CORS_ORIGINS.split(",")
        for origin in origins_raw:
            origins.append(origin.strip())
        application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


app = get_application()


@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    detail = err.args[0]
    if isinstance(detail, list) or isinstance(detail, tuple):
        detail = str(detail[0])
    if isinstance(detail, str):
        detail.replace('"', "'").replace("\n", " ")
    error = f"Failed to execute {request.method} on {request.url}: {detail}"
    logging.error(error)
    return JSONResponse(status_code=500, content={"error": error})


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="info")
