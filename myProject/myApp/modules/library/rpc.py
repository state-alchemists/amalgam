from modules.library.book import BookService, register_book_rpc
from typing import Mapping, List, Any
from core import AuthService
from helpers.transport import RPC, MessageBus

import traceback
import sys

# Note: 💀 Don't delete the following line, Zaruba use it for pattern matching
def register_library_rpc_handler(mb: MessageBus, rpc: RPC, auth_service: AuthService, book_service: BookService):

    register_book_rpc(mb, rpc, auth_service, book_service)

    print('Register library RPC handler', file=sys.stderr)
