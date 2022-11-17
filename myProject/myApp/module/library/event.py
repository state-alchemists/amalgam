from typing import Mapping, List, Any
from core import AuthService
from transport import AppMessageBus, AppRPC

import traceback
import sys

# Note: 💀 Don't delete the following line; Zaruba uses it for pattern matching
def register_library_event_handler(mb: AppMessageBus, rpc: AppRPC, auth_service: AuthService):

    print('Register library event handler', file=sys.stderr)
