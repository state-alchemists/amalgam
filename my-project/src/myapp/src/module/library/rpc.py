from logging import Logger
from typing import Any

from core.messagebus import Publisher
from core.rpc import Caller, Server
from module.library.entity.book.rpc import register_rpc as register_book_rpc


def register_rpc(
    logger: Logger, rpc_server: Server, rpc_caller: Caller, publisher: Publisher
):
    logger.info('🥪 Register RPC handlers for "library"')
    register_book_rpc(logger, rpc_server, rpc_caller, publisher)
