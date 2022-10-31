from typing import Tuple
from helpers.transport import RPC, LocalRPC
from core.security.rule.defaultAuthRule import DefaultAuthRule
from modules.auth.user.test_defaultUserService_util import AUTHORIZED_ACTIVE_USER, AUTHORIZED_INACTIVE_USER
from schemas.user import User, UserData


def create_rpc() -> RPC:
    rpc = LocalRPC()
    # handle is_user_authorized
    @rpc.handle('is_user_authorized')
    def is_user_authorized(user_data: UserData, permission: str) -> bool:
        user = User.parse_obj(user_data)
        return user.id in [AUTHORIZED_ACTIVE_USER.id, AUTHORIZED_INACTIVE_USER]
    # return rpc
    return rpc


def init_test_default_auth_rule_components() -> Tuple[DefaultAuthRule, RPC]:
    rpc = create_rpc()
    default_auth_rule = DefaultAuthRule(rpc)
    return default_auth_rule, rpc
    
