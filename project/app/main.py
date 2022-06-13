"""Main module"""
import logging
import os
import time

from fastapi import FastAPI, Request

from api import auth, article
from db import init_db


log = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    application = FastAPI(
        docs_url=os.getenv("SWAGGER_PATH"),
        redoc_url=os.getenv("REDOC_PATH"),
        openapi_url=os.getenv("OPENAPI_PATH"),
        title="SimpleCMS",
        version="0.1")
    application.include_router(auth.router, prefix="/auth", tags=["auth"])
    application.include_router(article.router,
                               prefix="/article", tags=["article"])

    return application


app = create_app()


@app.middleware('http')
async def x_process_time_middleware(request: Request, call_next):
    """X-Process-Time header shows how many seconds we spend
    to every request"""
    start_time = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(
        time.perf_counter()-start_time)
    return response


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
