from myapp.config import APP_LIBRARY_BASE_URL
from myapp.module.library.client.library_client import LibraryClient
from myapp.module.library.service.book.book_service_factory import book_service

book_api_client = book_service.as_api_client(base_url=APP_LIBRARY_BASE_URL)


class LibraryAPIClient(book_api_client, LibraryClient):
    pass
