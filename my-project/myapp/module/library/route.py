from fastapi import FastAPI

from myapp.common.app_factory import app
from myapp.common.schema import BasicResponse
from myapp.config import APP_MAIN_MODULE, APP_MODE, APP_MODULES
from myapp.module.library.service.book.book_service_factory import book_service


def serve_route(app: FastAPI):
    if APP_MODE != "microservices" or "library" not in APP_MODULES:
        return
    if APP_MAIN_MODULE == "library":
        _serve_health_check(app)
        _serve_readiness_check(app)
    book_service.serve_route(app)


def _serve_health_check(app: FastAPI):
    @app.api_route("/health", methods=["GET", "HEAD"], response_model=BasicResponse)
    async def health():
        """
        Microservice's health check
        """
        return BasicResponse(message="ok")


def _serve_readiness_check(app: FastAPI):
    @app.api_route("/readiness", methods=["GET", "HEAD"], response_model=BasicResponse)
    async def readiness():
        """
        Microservice's readiness check
        """
        return BasicResponse(message="ok")


serve_route(app)
