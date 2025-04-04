from myapp.config import APP_COMMUNICATION
from myapp.module.library.client.library_api_client import LibraryAPIClient
from myapp.module.library.client.library_client import LibraryClient
from myapp.module.library.client.library_direct_client import (
    LibraryDirectClient,
)

if APP_COMMUNICATION == "direct":
    library_client: LibraryClient = LibraryDirectClient()
elif APP_COMMUNICATION == "api":
    library_client: LibraryClient = LibraryAPIClient()
