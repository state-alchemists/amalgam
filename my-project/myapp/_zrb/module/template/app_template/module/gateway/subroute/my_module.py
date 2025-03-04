import os
from typing import Annotated

from fastapi import Depends, FastAPI

from myapp.common.error import ForbiddenError
from myapp.module.gateway.util.auth import get_current_user
from myapp.module.gateway.util.view import render_content, render_error
from myapp.schema.user import AuthUserResponse


def serve_my_module_route(app: FastAPI):
    """
    Serving routes for my_module
    """
