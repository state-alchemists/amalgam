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

# create myApp application + it's runner
# myApp application should contain a library module that serve books CRUD
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

# add simple homepage
echo "👷 Add homepage"
zaruba please addFastAppPage \
    appDirectory=myApp \
    appModuleName=library \
    appHttpMethod=get \
    appUrl=/

echo "👷 Generate myAppMigration"
zaruba please createMyAppMigration

echo "👷 Update myAppMigration file"
# Look for newly generated migration file and change:
#   return os.getenv('MIGRATION_RUN_ALL', '0') != '0'
# into:
#   return os.getenv('MIGRATION_RUN_ALL', '0') != '0' or os.getenv('APP_ENABLE_LIBRARY_MODULE', '1') != '0'
MIGRATION_PATH=myApp/alembic/versions
for MIGRATION_FILE in $(zaruba file list "${MIGRATION_PATH}")
do
    if [ -f "${MIGRATION_PATH}/${MIGRATION_FILE}" ]
    then
        MATCH=$(zaruba str submatch "$(cat "${MIGRATION_PATH}/${MIGRATION_FILE}")" "op\.create_table\('books',")
        if [ "${MATCH}" != "null" ]
        then
            MIGRATION_LINES=$(zaruba lines read "${MIGRATION_PATH}/${MIGRATION_FILE}")
            LINE_INDEX=$(zaruba lines getIndex "${MIGRATION_LINES}" "(\w*)return os.getenv\('MIGRATION_RUN_ALL'")
            if [ "${LINE_INDEX}" = -1 ]
            then
                echo "Pattern not found"
                exit 1
            fi
            MIGRATION_LINES=$(zaruba lines replace "${MIGRATION_LINES}" "${LINE_INDEX}" "    return os.getenv('MIGRATION_RUN_ALL', '0') != '0' or os.getenv('APP_ENABLE_LIBRARY_MODULE', '1') != '0'")
            zaruba lines write "${MIGRATION_PATH}/${MIGRATION_FILE}" "${MIGRATION_LINES}"
            break
        fi
    fi
done

echo "👷 Synchronize environment"
zaruba please syncEnv

echo "👷 This is enough for monolith app."
echo "👷 You can run the app natively: cd myProject && zaruba please startApp"
echo "👷 Or you can run the app as container: cd myProject && zaruba please startAppContainer"
echo "👷 Once running, you can visit: http://localhost:3000"


################################################################################################
# Add sql and rabbitmq to the project
################################################################################################

# We want to split myApp into several microservices:
# - frontend (visual matters)
# - backend (API gateway)
# - authSvc (handle auth and user activities)
# - libSvc (handle book CRUD)
#
# We need RabbitMQ to let our services talk to each others
# We also need MySQL Database for authSvc and libSvc

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

# MyFrontend has the same code base as myApp.
# It focused on visual matters.
# Thus, we need to disable API, RPC handler, and event handler.

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
zaruba task setEnv startMyFrontend APP_DB_CREATE_ALL 0
zaruba task setEnv startMyFrontend MIGRATION_RUN_ALL 0

zaruba task addDependencies prepareMyFrontend prepareMyApp
zaruba task setConfig prepareMyFrontend start 'echo "Done"'
zaruba task addDependencies migrateMyFrontend migrateMyApp
zaruba task setConfig migrateMyFrontend start 'echo "Done"'

zaruba task addDependencies startMyFrontend startMyRabbitmq
zaruba task addDependencies startMyFrontendContainer startMyRabbitmqContainer

################################################################################################
# Add backend runner
################################################################################################

# MyBackend is an API gateway.
# It takes request from myFrontend, and emit events or invoke RPC call to be handled by MyAuthSvc and MyLibSvc
# Thus, we need to disable the UI, RPC handler, and event handler.

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
zaruba task setEnv startMyBackend APP_DB_CREATE_ALL 0
zaruba task setEnv startMyBackend MIGRATION_RUN_ALL 0

zaruba task addDependencies prepareMyBackend prepareMyApp
zaruba task setConfig prepareMyBackend start 'echo "Done"'
zaruba task addDependencies migrateMyBackend migrateMyApp
zaruba task setConfig migrateMyBackend start 'echo "Done"'

zaruba task addDependencies startMyBackend startMyRabbitmq
zaruba task addDependencies startMyBackendContainer startMyRabbitmqContainer


################################################################################################
# Add authSvc runner
################################################################################################

# MyAuthSvc serve authentication and logging.
# It handle RPC calls and event from MyBackend and other internal services
# Thus, we need to disable the UI and API handler.
# We also need to make sure that MyAuthSvc only have Auth module enabled.

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
zaruba task setEnv startMyAuthSvc APP_DB_CREATE_ALL 0
zaruba task setEnv startMyAuthSvc MIGRATION_RUN_ALL 0

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

# MyLibSvc serve book CRUD.
# It handle RPC calls and event from MyBackend and other internal services
# Thus, we need to disable the UI and API handler.
# We also need to make sure that MyAuthSvc only have library module enabled.

echo "👷 Add libSvc"
zaruba please makeFastAppRunner \
    appDirectory=myApp \
    appName=myLibSvc

zaruba task setEnv startMyLibSvc APP_HTTP_PORT 3004
zaruba task setEnv startMyLibSvc APP_ENABLE_ROUTE_HANDLER 0
zaruba task setEnv startMyLibSvc APP_ENABLE_UI 0
zaruba task setEnv startMyLibSvc APP_ENABLE_API 0
zaruba task setEnv startMyLibSvc APP_ENABLE_AUTH_MODULE 0
zaruba task setEnv startMyLibSvc APP_ENABLE_LOG_MODULE 0
zaruba task setEnv startMyLibSvc APP_RPC_TYPE rmq
zaruba task setEnv startMyLibSvc APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv startMyLibSvc APP_RABBITMQ_HOST localhost
zaruba task setEnv startMyLibSvc APP_RABBITMQ_USER root
zaruba task setEnv startMyLibSvc APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv startMyLibSvc APP_RABBITMQ_VHOST /
zaruba task setEnv startMyLibSvc APP_SQLALCHEMY_DATABASE_URL 'mysql+pymysql://root:Alch3mist@localhost:3308/sample?charset=utf8mb4'
zaruba task setEnv startMyLibSvc APP_SEED_ROOT_USER 0
zaruba task setEnv startMyLibSvc APP_DB_CREATE_ALL 0
zaruba task setEnv startMyLibSvc MIGRATION_RUN_ALL 0

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

# We want to run all microservices components by invoking single command:
# zaruba please startMyMicroservices
# Thus, we need to create the task and add other tasks as it dependencies.

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

echo "👷 Synchronize environment"
zaruba please syncEnv

echo "👷 This is enough for microservices app."
echo "👷 You can run the the microservices natively: cd myProject && zaruba please startMyMicroservices"
echo "👷 Or you can run the microservices as container: cd myProject && zaruba please startMyMicroservicesContainers"
echo "👷 Once running, you can visit:"
echo "👷    - http://localhost:3001 (frontend)"
echo "👷    - http://localhost:3002 (backend)"
echo "👷    - http://localhost:15672 (rabbitmq)"
echo "👷 To stop, you need to press ctrl+c and perform: zaruba please stopContainers"

################################################################################################
# Add Deployments
################################################################################################

# Now we are ready for kubernetes.
# We need to create several deployments to our services.

echo "👷 Set project values"
zaruba project setValue defaultKubeContext docker-desktop
zaruba project setValue pulumiUseLocalBackend yes

echo "👷 Add auth svc db deployment"
zaruba please addMysqlHelmDeployment deploymentDirectory=myAuthSvcDbDeployment
zaruba task setEnv deployMyAuthSvcDbDeployment FULLNAMEOVERRIDE "auth-svc-db"
zaruba task setEnv deployMyAuthSvcDbDeployment AUTH_DATABASE "auth"

echo "👷 Add lib svc db deployment"
zaruba please addMysqlHelmDeployment deploymentDirectory=myLibSvcDbDeployment
zaruba task setEnv deployMyLibSvcDbDeployment FULLNAMEOVERRIDE "lib-svc-db"
zaruba task setEnv deployMyLibSvcDbDeployment AUTH_DATABASE "lib"

echo "👷 Add rabbitmq deployment"
zaruba please addRabbitmqHelmDeployment deploymentDirectory=myRabbitmqDeployment
zaruba task setEnv deployMyRabbitmqDeployment FULLNAMEOVERRIDE "rabbitmq"

echo "👷 Add auth svc deployment"

zaruba please addAppHelmDeployment \
    appDirectory=myApp \
    deploymentDirectory=myAuthSvcDeployment \
    appPorts='["3000"]'

zaruba task setEnv deployMyAuthSvcDeployment LIVENESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyAuthSvcDeployment READINESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyAuthSvcDeployment SERVICE_ENABLED False
zaruba task setEnv deployMyAuthSvcDeployment FULLNAME_OVERRIDE auth-svc
zaruba task setEnv prepareMyAuthSvcDeployment APP_HTTP_PORT 3000
zaruba task setEnv prepareMyAuthSvcDeployment APP_ENABLE_ROUTE_HANDLER 0
zaruba task setEnv prepareMyAuthSvcDeployment APP_ENABLE_UI 0
zaruba task setEnv prepareMyAuthSvcDeployment APP_ENABLE_API 0
zaruba task setEnv prepareMyAuthSvcDeployment APP_ENABLE_LIBRARY_MODULE 0
zaruba task setEnv prepareMyAuthSvcDeployment APP_RPC_TYPE rmq
zaruba task setEnv prepareMyAuthSvcDeployment APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv prepareMyAuthSvcDeployment APP_RABBITMQ_HOST rabbitmq
zaruba task setEnv prepareMyAuthSvcDeployment APP_RABBITMQ_USER root
zaruba task setEnv prepareMyAuthSvcDeployment APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv prepareMyAuthSvcDeployment APP_RABBITMQ_VHOST /
zaruba task setEnv prepareMyAuthSvcDeployment APP_SQLALCHEMY_DATABASE_URL "mysql+pymysql://root:Alch3mist@auth-svc-db/auth?charset=utf8mb4"
zaruba task setEnv prepareMyAuthSvcDeployment APP_RABBITMQ_HOST "rabbitmq"

echo "👷 Add lib svc deployment"

zaruba please addAppHelmDeployment \
    appDirectory=myApp \
    deploymentDirectory=myLibSvcDeployment\
    appPorts='["3000"]'

zaruba task setEnv deployMyLibSvcDeployment LIVENESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyLibSvcDeployment READINESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyLibSvcDeployment SERVICE_ENABLED False
zaruba task setEnv deployMyLibSvcDeployment FULLNAME_OVERRIDE lib-svc
zaruba task setEnv prepareMyLibSvcDeployment APP_HTTP_PORT 3000
zaruba task setEnv prepareMyLibSvcDeployment APP_ENABLE_ROUTE_HANDLER 0
zaruba task setEnv prepareMyLibSvcDeployment APP_ENABLE_UI 0
zaruba task setEnv prepareMyLibSvcDeployment APP_ENABLE_API 0
zaruba task setEnv prepareMyLibSvcDeployment APP_ENABLE_AUTH_MODULE 0
zaruba task setEnv prepareMyLibSvcDeployment APP_ENABLE_LOG_MODULE 0
zaruba task setEnv prepareMyLibSvcDeployment APP_RPC_TYPE rmq
zaruba task setEnv prepareMyLibSvcDeployment APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv prepareMyLibSvcDeployment APP_RABBITMQ_HOST rabbitmq
zaruba task setEnv prepareMyLibSvcDeployment APP_RABBITMQ_USER root
zaruba task setEnv prepareMyLibSvcDeployment APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv prepareMyLibSvcDeployment APP_RABBITMQ_VHOST /
zaruba task setEnv prepareMyLibSvcDeployment APP_SQLALCHEMY_DATABASE_URL "mysql+pymysql://root:Alch3mist@lib-svc-db/lib?charset=utf8mb4"

echo "👷 Add frontend deployment"

zaruba please addAppHelmDeployment \
    appDirectory=myApp \
    deploymentDirectory=myFrontendDeployment \
    appPorts='["3001"]'

zaruba task setEnv deployMyFrontendDeployment LIVENESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyFrontendDeployment READINESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyFrontendDeployment SERVICE_TYPE LoadBalancer
zaruba task setEnv deployMyFrontendDeployment SERVICE_ENABLED True
zaruba task setEnv deployMyFrontendDeployment FULLNAME_OVERRIDE frontend
zaruba task setEnv prepareMyFrontendDeployment APP_HTTP_PORT 3001
zaruba task setEnv prepareMyFrontendDeployment APP_ENABLE_API 0
zaruba task setEnv prepareMyFrontendDeployment APP_ENABLE_RPC_HANDLER 0
zaruba task setEnv prepareMyFrontendDeployment APP_ENABLE_EVENT_HANDLER 0
zaruba task setEnv prepareMyFrontendDeployment APP_RPC_TYPE rmq
zaruba task setEnv prepareMyFrontendDeployment APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv prepareMyFrontendDeployment APP_RABBITMQ_HOST rabbitmq
zaruba task setEnv prepareMyFrontendDeployment APP_RABBITMQ_USER root
zaruba task setEnv prepareMyFrontendDeployment APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv prepareMyFrontendDeployment APP_RABBITMQ_VHOST /
zaruba task setEnv prepareMyFrontendDeployment APP_UI_BACKEND_URL http://localhost:3002
zaruba task setEnv prepareMyFrontendDeployment APP_SEED_ROOT_USER 0

echo "👷 Add backend deployment"
zaruba please addAppHelmDeployment \
    appDirectory=myApp \
    deploymentDirectory=myBackendDeployment \
    appPorts='["3002"]'

zaruba task setEnv deployMyBackendDeployment LIVENESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyBackendDeployment READINESS_PROBE_HTTP_GET_PATH /readiness
zaruba task setEnv deployMyBackendDeployment SERVICE_TYPE LoadBalancer
zaruba task setEnv deployMyBackendDeployment SERVICE_ENABLED True
zaruba task setEnv deployMyBackendDeployment FULLNAME_OVERRIDE backend
zaruba task setEnv prepareMyBackendDeployment APP_HTTP_PORT 3002
zaruba task setEnv prepareMyBackendDeployment APP_ENABLE_UI 0
zaruba task setEnv prepareMyBackendDeployment APP_ENABLE_RPC_HANDLER 0
zaruba task setEnv prepareMyBackendDeployment APP_ENABLE_EVENT_HANDLER 0
zaruba task setEnv prepareMyBackendDeployment APP_RPC_TYPE rmq
zaruba task setEnv prepareMyBackendDeployment APP_MESSAGE_BUS_TYPE rmq
zaruba task setEnv prepareMyBackendDeployment APP_RABBITMQ_HOST rabbitmq
zaruba task setEnv prepareMyBackendDeployment APP_RABBITMQ_USER root
zaruba task setEnv prepareMyBackendDeployment APP_RABBITMQ_PASS Alch3mist
zaruba task setEnv prepareMyBackendDeployment APP_RABBITMQ_VHOST /
zaruba task setEnv prepareMyBackendDeployment APP_SEED_ROOT_USER 0

echo "👷 Synchronize environment"
zaruba please syncEnv

echo "👷 Build image"
zaruba please buildImages

echo "👷 Prepare deployments"
zaruba please prepareDeployments

echo "👷 This is enough for deployment."
echo "👷 To deploy, you can run: cd myProject && zaruba please deploy"
echo "👷 Once running, you can visit:"
echo "👷    - http://localhost:3001 (frontend)"
echo "👷    - http://localhost:3002 (backend)"
echo "👷 To destroy, you perform: zaruba please destroy"

