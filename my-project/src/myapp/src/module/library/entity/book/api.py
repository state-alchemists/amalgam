from logging import Logger

from component.error import HTTPAPIException
from component.messagebus import Publisher
from component.rpc import Caller
from fastapi import Depends, FastAPI
from module.auth.component import Authorizer
from module.auth.integration import access_token_scheme
from module.auth.schema.token import AccessTokenData
from module.library.schema.book import (
    Book,
    BookData,
    BookResult,
)


def register_api(
    logger: Logger,
    app: FastAPI,
    authorizer: Authorizer,
    rpc_caller: Caller,
    publisher: Publisher,
):
    logger.info('🥪 Register API for "library.book"')

    @app.get(
        "/api/v1/library/books",
        response_model=BookResult,
    )
    async def get_books(
        keyword: str = "",
        limit: int = 100,
        offset: int = 0,
        user_token_data: AccessTokenData = Depends(access_token_scheme),
    ):
        if not await authorizer.is_having_permission(
            user_token_data.user_id, "library:book:get"
        ):
            raise HTTPAPIException(403, "Unauthorized")
        try:
            result_dict = await rpc_caller.call(
                "library_get_book",
                keyword=keyword,
                criterion={},
                limit=limit,
                offset=offset,
                user_token_data=user_token_data.model_dump(),
            )
            return BookResult(**result_dict)
        except Exception as e:
            raise HTTPAPIException(error=e)

    @app.get(
        "/api/v1/library/books/{id}",
        response_model=Book,
    )
    async def get_book_by_id(
        id: str, user_token_data: AccessTokenData = Depends(access_token_scheme)
    ):
        if not await authorizer.is_having_permission(
            user_token_data.user_id,
            "library:book:get_by_id",
        ):
            raise HTTPAPIException(403, "Unauthorized")
        try:
            result_dict = await rpc_caller.call(
                "library_get_book_by_id",
                id=id,
                user_token_data=user_token_data.model_dump(),
            )
            return Book(**result_dict)
        except Exception as e:
            raise HTTPAPIException(error=e)

    @app.post(
        "/api/v1/library/books",
        response_model=Book,
    )
    async def insert_book(
        data: BookData,
        user_token_data: AccessTokenData = Depends(access_token_scheme),
    ):
        if not await authorizer.is_having_permission(
            user_token_data.user_id,
            "library:book:insert",
        ):
            raise HTTPAPIException(403, "Unauthorized")
        try:
            result_dict = await rpc_caller.call(
                "library_insert_book",
                data=data.model_dump(),
                user_token_data=user_token_data.model_dump(),
            )
            return Book(**result_dict)
        except Exception as e:
            raise HTTPAPIException(error=e)

    @app.put(
        "/api/v1/library/books/{id}",
        response_model=Book,
    )
    async def update_book(
        id: str,
        data: BookData,
        user_token_data: AccessTokenData = Depends(access_token_scheme),
    ):
        if not await authorizer.is_having_permission(
            user_token_data.user_id,
            "library:book:update",
        ):
            raise HTTPAPIException(403, "Unauthorized")
        try:
            result_dict = await rpc_caller.call(
                "library_update_book",
                id=id,
                data=data.model_dump(),
                user_token_data=user_token_data.model_dump(),
            )
            return Book(**result_dict)
        except Exception as e:
            raise HTTPAPIException(error=e)

    @app.delete(
        "/api/v1/library/books/{id}",
        response_model=Book,
    )
    async def delete_book(
        id: str, user_token_data: AccessTokenData = Depends(access_token_scheme)
    ):
        if not await authorizer.is_having_permission(
            user_token_data.user_id,
            "library:book:delete",
        ):
            raise HTTPAPIException(403, "Unauthorized")
        try:
            result_dict = await rpc_caller.call(
                "library_delete_book",
                id=id,
                user_token_data=user_token_data.model_dump(),
            )
            return Book(**result_dict)
        except Exception as e:
            raise HTTPAPIException(error=e)
