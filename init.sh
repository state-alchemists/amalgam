set -e

if [ -d "my-project" ]
then
    echo "👷 Remove my-project directory"
    sudo rm -Rf my-project
fi

echo "👷 Create my-project"
zrb project create --project-dir my-project --project "My Project"
cd my-project

echo "👷 Add fastapp"
zrb project add fastapp --project-dir . --app "myapp"

echo "👷 Add library module"
zrb project myapp create module --module library

echo "👷 Add book entity"
zrb project myapp create entity --module library --entity book --plural books --column isbn

echo "👷 Add title field"
zrb project myapp create column --module library --entity book --column title --type str

echo "👷 Add author field"
zrb project myapp create column --module library --entity book --column author --type str

echo "👷 Start fastapp"
export MYAPP_AUTH_SUPER_ADMIN_PASSWORD=admin
zrb project myapp run all --env dev
