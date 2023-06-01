from typing import Any, Mapping
from logging import Logger
from core.messagebus import Publisher
from core.rpc import Caller, Server
from core.repo import SearchFilter
from module.library.component.model.book_model import (
    book_model
)
from module.library.schema.book import BookData
from module.auth.schema.token import AccessTokenData


def register_rpc(
    logger: Logger,
    rpc_server: Server,
    rpc_caller: Caller,
    publisher: Publisher
):
    logger.info('🥪 Register RPC handlers for "library.book"')

    @rpc_server.register('library_get_book')
    async def get(
        keyword: str,
        criterion: Mapping[str, Any],
        limit: int,
        offset: int,
        user_token_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        result = await book_model.get(
            search_filter=SearchFilter(
                keyword=keyword, criterion=criterion
            ),
            limit=limit,
            offset=offset
        )
        return result.dict()

    @rpc_server.register('library_get_book_by_id')
    async def get_by_id(
        id: str,
        user_token_data: Mapping[str, Any] = {}
    ) -> Mapping[str, Any]:
        row = await book_model.get_by_id(id)
        return row.dict()

    @rpc_server.register('library_insert_book')
    async def insert(
        data: Mapping[str, Any],
        user_token_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        user_token_data = AccessTokenData(**user_token_data)
        data['created_by'] = user_token_data.user_id
        data['updated_by'] = user_token_data.user_id
        row = await book_model.insert(
            data=BookData(**data)
        )
        return row.dict()

    @rpc_server.register('library_update_book')
    async def update(
        id: str,
        data: Mapping[str, Any],
        user_token_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        user_token_data = AccessTokenData(**user_token_data)
        data['updated_by'] = user_token_data.user_id
        row = await book_model.update(
            id=id, data=BookData(**data)
        )
        return row.dict()

    @rpc_server.register('library_delete_book')
    async def delete(
        id: str,
        user_token_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        user_token_data = AccessTokenData(**user_token_data)
        row = await book_model.delete(id=id)
        return row.dict()
