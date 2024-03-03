from logging import Logger

from component.messagebus import Publisher
from component.rpc import Caller
from fastapi import FastAPI
from module.auth.component import Authorizer
from module.library.entity.book.api import register_api as register_book_api


def register_api(
    logger: Logger,
    app: FastAPI,
    authorizer: Authorizer,
    rpc_caller: Caller,
    publisher: Publisher,
):
    logger.info('🥪 Register API for "library"')
    register_book_api(logger, app, authorizer, rpc_caller, publisher)
