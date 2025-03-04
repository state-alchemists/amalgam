from myapp.config import APP_COMMUNICATION
from myapp.module.my_module.client.my_module_api_client import MyModuleAPIClient
from myapp.module.my_module.client.my_module_client import MyModuleClient
from myapp.module.my_module.client.my_module_direct_client import MyModuleDirectClient

if APP_COMMUNICATION == "direct":
    my_module_client: MyModuleClient = MyModuleDirectClient()
elif APP_COMMUNICATION == "api":
    my_module_client: MyModuleClient = MyModuleAPIClient()
