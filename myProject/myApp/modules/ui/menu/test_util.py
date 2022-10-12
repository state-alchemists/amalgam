from typing import Callable, Optional, Tuple, List, Mapping
from modules.ui.menu.menuService import MenuService
from modules.auth.auth.authService import AuthService
from modules.auth.user.test_util import GUEST_USER, UNAUTHORIZED_ACTIVE_USER, AUTHORIZED_ACTIVE_USER
from helpers.transport.localRpc import LocalRPC
from schemas.user import User, UserData
from schemas.menu import Menu
from starlette.requests import Request
from fastapi import HTTPException
from schemas.authType import AuthType

class MockAuthService(AuthService):

    def __init__(self, user: Optional[User]):
        self.user = user
    
    def _return_none_or_throw_error(throw_error: bool):
        if not throw_error:
            return False
        raise HTTPException(status_code=402, detail='Unauthroized')

    def everyone(self, throw_error: bool = True) -> Callable[[Request], Optional[User]]:
        def verify_everyone(request: Optional[Request]) -> Optional[User]:
            if self.user is None:
                return GUEST_USER
            return self.user
        return verify_everyone

    def is_authenticated(self, throw_error: bool = True) -> Callable[[Request], Optional[User]]:
        def verify_authenticated(request: Optional[Request]) -> Optional[User]:
            if self.user == UNAUTHORIZED_ACTIVE_USER or self.user == AUTHORIZED_ACTIVE_USER:
                return self.user
            return self._return_none_or_throw_error(throw_error)
        return verify_authenticated

    def is_unauthenticated(self, throw_error: bool = True) -> Callable[[Request], Optional[User]]:
        def verify_unauthenticated(request: Optional[Request]) -> Optional[User]:
            if self.user is None or self.user == GUEST_USER:
                return self.user
            return self._return_none_or_throw_error(throw_error)
        return verify_unauthenticated

    def is_authorized(self, permission: str, throw_error: bool = True) -> Callable[[Request], Optional[User]]:
        def verify_authorized(request: Optional[Request]) -> Optional[User]:
            if self.user == AUTHORIZED_ACTIVE_USER:
                return self.user
            return self._return_none_or_throw_error(throw_error)
        return verify_authorized


menu_mock_rpc = LocalRPC()

@menu_mock_rpc.handle('is_user_authorized')
def is_user_authorized(user_data: UserData, permission: str) -> bool:
    user = User.parse_obj(user_data)
    return user.id == AUTHORIZED_ACTIVE_USER.id


class SingleMenuTestCase():
    def __init__(self, name: str, is_highlighted: bool, submenus_count: int = 0):
        self.name = name
        self.is_highlighted = is_highlighted
        self.submenus_count = submenus_count

    def assert_menu(self, menu = Menu):
        assert menu.name == self.name
        assert menu.is_highlighted == self.is_highlighted
        assert len(menu.submenus) == self.submenus_count 


class MenuTestCase(SingleMenuTestCase):
    def __init__(self, name: str, is_highlighted: bool, submenus_count: int = 0, children: List[SingleMenuTestCase] = []):
        super().__init__(name, is_highlighted, submenus_count)
        self.children = children
    
    def assert_menu(self, menu = Menu):
        super().assert_menu(menu)
        for child_index, child in enumerate(self.children):
            child.assert_menu(menu.submenus[child_index])


async def check_is_authorized(menu_service: MenuService, user: Optional[User], accessibility_test_cases: Mapping[str, bool] = {}):
    for menu_name, expectation in accessibility_test_cases.items():
        if expectation:
            authorize = menu_service.is_authorized(menu_name)
            menu_context = await authorize(current_user = user)
            assert menu_context.current_user == user
            continue
        is_error = False
        try:
            authorize = menu_service.is_authorized(menu_name)
            menu_context = await authorize(current_user = user)
        except:
            is_error = True
        assert is_error


def init_test_menu_service_components(user: Optional[User]) -> Tuple[MenuService, MockAuthService]:
    auth_service = MockAuthService(user)
    menu_service = MenuService(menu_mock_rpc, auth_service)
    return menu_service, auth_service


def init_test_menu_data(menu_service: MenuService):
    '''
    This will generate all possible combination of two level menu:
        - everyone (AuthType.EVERYONE)
            - everyone-everyone (AuthType.EVERYONE)
            - everyone-unauthenticated (AuthType.UNAUTHENTICATED)
            - everyone-authenticated (AuthType.AUTHENTICATED)
            - everyone-authorized (AuthType.AUTHORIZED)
        - unauthenticated (AuthType.UNAUTHENTICATED)
            - unauthenticated-everyone (AuthType.EVERYONE)
            - unauthenticated-unauthenticated (AuthType.UNAUTHENTICATED)
            - unauthenticated-authenticated (AuthType.AUTHENTICATED)
            - unauthenticated-authorized (AuthType.AUTHORIZED)
        ...
        - authorized (AuthType.AUTHORIZED)
            ...
            - authorized-authorized (AuthType.AUTHORIZED)
    '''
    auth_type_map = {
        'everyone': AuthType.EVERYONE,
        'unauthenticated': AuthType.UNAUTHENTICATED,
        'authenticated': AuthType.AUTHENTICATED,
        'authorized': AuthType.AUTHORIZED,
    }
    for parent_key in auth_type_map:
        parent_menu_name = parent_key
        parent_menu_title = parent_menu_name
        parent_menu_url = '/{}'.format(parent_key)
        parent_menu_auth_type = auth_type_map[parent_key]
        menu_service.add_menu(parent_menu_name, title=parent_menu_title, url=parent_menu_url, auth_type=parent_menu_auth_type)
        for child_key in auth_type_map:
            child_menu_name = '{}-{}'.format(parent_key, child_key)
            child_menu_title = child_menu_name
            child_menu_url = '/{}/{}'.format(parent_key, child_key)
            child_menu_auth_type = auth_type_map[child_key]
            menu_service.add_menu(child_menu_name, title=child_menu_title, url=child_menu_url, auth_type=child_menu_auth_type, parent_name=parent_menu_name)