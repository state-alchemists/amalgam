from repos.book import BookRepo
from library.bookRpc import register_book_rpc
from typing import Mapping, List, Any
from helpers.transport import RPC

import traceback
import sys

def register_library_rpc_handler(rpc: RPC, book_repo: BookRepo):

    register_book_rpc(rpc, book_repo)

    print('Register library RPC handler')
