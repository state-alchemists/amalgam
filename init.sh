set -e

################################################################################################
# Create project
################################################################################################

# re-create Project directory
if [ -d "myProject" ]
then
    echo "👷 Remove myProject directory"
    sudo rm -Rf myProject
fi
echo "👷 Create Project directory"
mkdir -p myProject

# make Project a zaruba project
echo "👷 Make Project a zaruba project"
cd myProject
zaruba please initProject

# we don't want Project to be a git subrepository
echo "👷 Remove Project/.git"
rm -Rf .git


################################################################################################
# Add application and monolith runner to the project
################################################################################################

# create App application + it's runner
# App application should contain a library module that serve books CRUD
echo "👷 Add App application + it's runner"
zaruba please addFastAppCrud \
    appDirectory=myApp \
    appModuleName=library \
    appCrudEntity=books \
    appCrudFields='["title", "author"]'

# add synopsis field to the crud
echo "👷 Add synopsis field to Book Entity"
zaruba please addFastAppCrudField \
    appDirectory=myApp \
    appModuleName=library \
    appCrudEntity=books \
    appCrudField=synopsis

echo "👷 Add homepage"
zaruba please addFastAppPage \
    appDirectory=myApp \
    appModuleName=library \
    appHttpMethod=get \
    appUrl=/

echo "👷 Generate myAppMigration"
zaruba please createMyAppMigration

echo "👷 This is enough for monolith app."
echo "👷 You can run the app natively: cd myProject && zaruba please startApp"
echo "👷 Or you can run the app as container: cd myProject && zaruba please startAppContainer"
echo "👷 Once running, you can visit: http://localhost:3000"


################################################################################################
# Add sql and rabbitmq to the project
################################################################################################

echo "👷 Add mysql for authSvc"
zaruba please addMysql \
    appDirectory=myAuthSvcDb \
    appPorts='["3307:3306"]'
zaruba task setConfig startMyAuthSvcDbContainer afterCheck 'sleep 10'

echo "👷 Add mysql for libSvc"
zaruba please addMysql \
    appDirectory=myLibSvcDb \
    appPorts='["3308:3306"]'
zaruba task setConfig startMyLibSvcDbContainer afterCheck 'sleep 10'

echo "👷 Add rabbitmq"
zaruba please addRabbitmq appDirectory=myRabbitmq
zaruba task setConfig startMyRabbitmqContainer afterCheck 'sleep 15'


################################################################################################
# Add frontend runner
################################################################################################

echo "👷 Add frontend"
zaruba please makeFastAppRunner \
    appDirectory=myApp \
    appName=myFrontend

zaruba task setEnv startMyFrontend APP_HTTP_PORT 3001
zaruba task setEnv startMyFrontend APP_ENABLE_API 0
zaruba task setEnv startMyFrontend APP_ENABLE_RPC_HANDLER 0
zaruba task setEnv startMyFrontend APP_ENABLE_EVENT_HANDLER 0
zaruba task setEnv startMyFrontend APP_RPC_TYPE rmq
zaruba task setEnv startMyFrontend APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv startMyFrontend APP_RABBITMQ_HOST localhost
zaruba task setEnv startMyFrontend APP_RABBITMQ_USER root
zaruba task setEnv startMyFrontend APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv startMyFrontend APP_RABBITMQ_VHOST /
zaruba task setEnv startMyFrontend APP_UI_BACKEND_URL http://localhost:3002
zaruba task setEnv startMyFrontend APP_SEED_ROOT_USER 0

zaruba task addDependencies prepareMyFrontend prepareMyApp
zaruba task setConfig prepareMyFrontend start 'echo "Done"'
zaruba task addDependencies migrateMyFrontend migrateMyApp
zaruba task setConfig migrateMyFrontend start 'echo "Done"'

zaruba task addDependencies startMyFrontend startMyRabbitmq
zaruba task addDependencies startMyFrontendContainer startMyRabbitmqContainer

################################################################################################
# Add backend runner
################################################################################################

echo "👷 Add backend"
zaruba please makeFastAppRunner \
    appDirectory=myApp \
    appName=myBackend

zaruba task setEnv startMyBackend APP_HTTP_PORT 3002
zaruba task setEnv startMyBackend APP_ENABLE_UI 0
zaruba task setEnv startMyBackend APP_ENABLE_RPC_HANDLER 0
zaruba task setEnv startMyBackend APP_ENABLE_EVENT_HANDLER 0
zaruba task setEnv startMyBackend APP_RPC_TYPE rmq
zaruba task setEnv startMyBackend APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv startMyBackend APP_RABBITMQ_HOST localhost
zaruba task setEnv startMyBackend APP_RABBITMQ_USER root
zaruba task setEnv startMyBackend APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv startMyBackend APP_RABBITMQ_VHOST /
zaruba task setEnv startMyBackend APP_SEED_ROOT_USER 0

zaruba task addDependencies prepareMyBackend prepareMyApp
zaruba task setConfig prepareMyBackend start 'echo "Done"'
zaruba task addDependencies migrateMyBackend migrateMyApp
zaruba task setConfig migrateMyBackend start 'echo "Done"'

zaruba task addDependencies startMyBackend startMyRabbitmq
zaruba task addDependencies startMyBackendContainer startMyRabbitmqContainer


################################################################################################
# Add authSvc runner
################################################################################################

echo "👷 Add authSvc"
zaruba please makeFastAppRunner \
    appDirectory=myApp \
    appName=myAuthSvc

zaruba task setEnv startMyAuthSvc APP_HTTP_PORT 3003
zaruba task setEnv startMyAuthSvc APP_ENABLE_ROUTE_HANDLER 0
zaruba task setEnv startMyAuthSvc APP_ENABLE_UI 0
zaruba task setEnv startMyAuthSvc APP_ENABLE_API 0
zaruba task setEnv startMyAuthSvc APP_ENABLE_LIBRARY_MODULE 0
zaruba task setEnv startMyAuthSvc APP_RPC_TYPE rmq
zaruba task setEnv startMyAuthSvc APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv startMyAuthSvc APP_RABBITMQ_HOST localhost
zaruba task setEnv startMyAuthSvc APP_RABBITMQ_USER root
zaruba task setEnv startMyAuthSvc APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv startMyAuthSvc APP_RABBITMQ_VHOST /
zaruba task setEnv startMyAuthSvc APP_SQLALCHEMY_DATABASE_URL 'mysql+pymysql://root:Alch3mist@localhost:3307/sample?charset=utf8mb4'

zaruba task addDependencies prepareMyAuthSvc prepareMyApp
zaruba task setConfig prepareMyAuthSvc start 'echo "Done"'

zaruba task addDependencies startMyAuthSvc startMyRabbitmq
zaruba task addDependencies startMyAuthSvcContainer startMyRabbitmqContainer
zaruba task addDependencies migrateMyAuthSvc startMyAuthSvcDb
zaruba task addDependencies startMyAuthSvc startMyAuthSvcDb
zaruba task addDependencies startMyAuthSvcContainer startMyAuthSvcDbContainer


################################################################################################
# Add libSvc runner
################################################################################################

echo "👷 Add libSvc"
zaruba please makeFastAppRunner \
    appDirectory=myApp \
    appName=myLibSvc

zaruba task setEnv startMyLibSvc APP_HTTP_PORT 3004
zaruba task setEnv startMyLibSvc APP_ENABLE_ROUTE_HANDLER 0
zaruba task setEnv startMyLibSvc APP_ENABLE_UI 0
zaruba task setEnv startMyLibSvc APP_ENABLE_API 0
zaruba task setEnv startMyLibSvc APP_ENABLE_AUTH_MODULE 0
zaruba task setEnv startMyLibSvc APP_RPC_TYPE rmq
zaruba task setEnv startMyLibSvc APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv startMyLibSvc APP_RABBITMQ_HOST localhost
zaruba task setEnv startMyLibSvc APP_RABBITMQ_USER root
zaruba task setEnv startMyLibSvc APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv startMyLibSvc APP_RABBITMQ_VHOST /
zaruba task setEnv startMyLibSvc APP_SQLALCHEMY_DATABASE_URL 'mysql+pymysql://root:Alch3mist@localhost:3308/sample?charset=utf8mb4'
zaruba task setEnv startMyLibSvc APP_SEED_ROOT_USER 0

zaruba task addDependencies prepareMyLibSvc prepareMyApp
zaruba task setConfig prepareMyLibSvc start 'echo "Done"'

zaruba task addDependencies startMyLibSvc startMyRabbitmq
zaruba task addDependencies migrateMyLibSvc startMyLibSvcDb
zaruba task addDependencies startMyLibSvcContainer startMyRabbitmqContainer
zaruba task addDependencies startMyLibSvc startMyLibSvcDb
zaruba task addDependencies startMyLibSvcContainer startMyLibSvcDbContainer

################################################################################################
# Add microservice runner
################################################################################################

echo "👷 Add microservice runner"
zaruba project addTask startMyMicroservices
zaruba project addTask startMyMicroservicesContainers
zaruba task addDependencies startMyMicroservices startMyFrontend
zaruba task addDependencies startMyMicroservicesContainers startMyFrontendContainer
zaruba task addDependencies startMyMicroservices startMyBackend
zaruba task addDependencies startMyMicroservicesContainers startMyBackendContainer
zaruba task addDependencies startMyMicroservices startMyAuthSvc
zaruba task addDependencies startMyMicroservicesContainers startMyAuthSvcContainer
zaruba task addDependencies startMyMicroservices startMyLibSvc
zaruba task addDependencies startMyMicroservicesContainers startMyLibSvcContainer


echo "👷 This is enough for microservices app."
echo "👷 You can run the the microservices natively: cd myProject && zaruba please startMyMicroservices"
echo "👷 Or you can run the microservices as container: cd myProject && zaruba please startMyMicroservicesContainers"
echo "👷 Once running, you can visit:"
echo "👷    - http://localhost:3001 (frontend)"
echo "👷    - http://localhost:3002 (backend)"
echo "👷    - http://localhost:15672 (rabbitmq)"
echo "👷 To stop, you need to press ctrl+c and perform: zaruba please stopContainers"

