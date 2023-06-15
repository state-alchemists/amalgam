set -e

if [ -d "my-project" ]
then
    echo "👷 Remove my-project directory"
    sudo rm -Rf my-project
fi

echo "👷 Crete my-project"
zrb project create --project-dir my-project --project-name "My Project"
cd my-project
rm -Rf .git

echo "👷 Add fastapp"
zrb project add fastapp --project-dir . --app-name "myapp" --http-port 3000

echo "👷 Add library module"
zrb project add fastapp-module --project-dir . --app-name "myapp" --module-name "library"

echo "👷 Add book entity"
zrb project add fastapp-crud --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --plural-entity-name "books" --column-name "code"

echo "👷 Add title field"
zrb project add fastapp-field --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --column-name "title" --column-type "str"

echo "👷 Start fastapp"
zrb project start-myapp --myapp-run-mode "monolith"
