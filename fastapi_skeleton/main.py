import asyncio

import nest_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from fastapi_skeleton.common.error.handler import add_http_exception_handler
from fastapi_skeleton.common.util.database import db
from fastapi_skeleton.config.config import Config
from fastapi_skeleton.container import Container
from fastapi_skeleton.router import example

nest_asyncio.apply()


def create_app() -> FastAPI:
    claon_app = FastAPI()

    """ Define Container """
    container = Container()
    claon_app.container = container

    """ Define Routers """
    api_version = "v1"
    api_prefix = "/api/" + api_version

    claon_app.include_router(example.router, prefix=api_prefix + "/examples")

    """ Define Middleware """
    claon_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    claon_app.add_middleware(SessionMiddleware, secret_key=Config.SESSION_SECRET_KEY)

    add_http_exception_handler(claon_app)

    return claon_app


app = create_app()


@app.on_event("startup")
async def startup():
    """ Initialize Database """
    asyncio.run(db.create_database())


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
