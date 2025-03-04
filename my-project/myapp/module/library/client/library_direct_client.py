from myapp.module.library.client.library_client import LibraryClient
from myapp.module.library.service.book.book_service_factory import book_service

book_direct_client = book_service.as_direct_client()


class LibraryDirectClient(book_direct_client, LibraryClient):
    pass
