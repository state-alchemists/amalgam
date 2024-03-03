from logging import Logger
from typing import Any, Mapping

from component.messagebus import Publisher
from component.repo import SearchFilter
from component.rpc import Caller, Server
from module.auth.schema.token import AccessTokenData
from module.library.integration.model.book_model import (
    book_model,
)
from module.library.schema.book import (
    BookData,
)


def register_rpc(
    logger: Logger, rpc_server: Server, rpc_caller: Caller, publisher: Publisher
):
    logger.info(
        '🥪 Register RPC handlers for "library.book"'
    )

    @rpc_server.register("library_get_book")
    async def get(
        keyword: str,
        criterion: Mapping[str, Any],
        limit: int,
        offset: int,
        user_token_data: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        result = await book_model.get(
            search_filter=SearchFilter(keyword=keyword, criterion=criterion),
            limit=limit,
            offset=offset,
        )
        return result.model_dump()

    @rpc_server.register("library_get_book_by_id")
    async def get_by_id(
        id: str, user_token_data: Mapping[str, Any] = {}
    ) -> Mapping[str, Any]:
        row = await book_model.get_by_id(id)
        return row.model_dump()

    @rpc_server.register("library_insert_book")
    async def insert(
        data: Mapping[str, Any], user_token_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        user_token_data = AccessTokenData(**user_token_data)
        data["created_by"] = user_token_data.user_id
        data["updated_by"] = user_token_data.user_id
        row = await book_model.insert(
            data=BookData(**data)
        )
        return row.model_dump()

    @rpc_server.register("library_update_book")
    async def update(
        id: str, data: Mapping[str, Any], user_token_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        user_token_data = AccessTokenData(**user_token_data)
        data["updated_by"] = user_token_data.user_id
        row = await book_model.update(
            id=id, data=BookData(**data)
        )
        return row.model_dump()

    @rpc_server.register("library_delete_book")
    async def delete(id: str, user_token_data: Mapping[str, Any]) -> Mapping[str, Any]:
        user_token_data = AccessTokenData(**user_token_data)
        row = await book_model.delete(id=id)
        return row.model_dump()
