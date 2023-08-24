"""
Module to create the FastAPI app and add the routes and middlewares
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError, ProgrammingError
import uvicorn
from src.errors import (
    operational_error_exc,
    programming_error_exc,
    custom_exc,
    CustomException,
)
from src.security import SecurityManager
#from src.routers import user_router, auth_router


def create_app():
    """Function to create the FastAPI app and add the routes and middlewares

    Returns:
        FastAPI: FastAPI app
    """
    SecurityManager.validate_env()

    app = FastAPI()

    #app.include_router(user_router.router)
    #app.include_router(auth_router.router)

    # disable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #healthcheck
    @app.get("/")
    async def root():
        return {"message": "Online"}
    
    @app.on_event("startup")
    async def startup_event():
        logger = logging.getLogger("uvicorn.access")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)

    add_exception_handlers(app)

    return app

def add_exception_handlers(app):
    """Function to add exception handlers to the app

    Args:
        app (FastAPI): FastAPI app
    """
    app.add_exception_handler(OperationalError, operational_error_exc)
    app.add_exception_handler(ProgrammingError, programming_error_exc)
    app.add_exception_handler(CustomException, custom_exc)

if __name__ == "__main__":
    uvicorn.run("src.main:create_app", host="0.0.0.0", port=5000, reload=True)