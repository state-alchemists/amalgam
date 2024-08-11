set -e

if [ -d "my-project" ]
then
    echo "👷 Remove my-project directory"
    sudo rm -Rf my-project
fi

echo "👷 Create my-project"
zrb project create --project-dir my-project --project-name "My Project"
cd my-project
rm -Rf .git

echo "👷 Add fastapp"
zrb project add fastapp app --project-dir . --app-name "myapp" --http-port 3000

echo "👷 Add library module"
zrb project add fastapp module --project-dir . --app-name "myapp" --module-name "library"

echo "👷 Add book entity"
zrb project add fastapp crud --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --plural-entity-name "books" --column-name "code"

echo "👷 Add title field"
zrb project add fastapp field --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --column-name "title" --column-type "string"

echo "👷 Add page_number field"
zrb project add fastapp field --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --column-name "page_number" --column-type "integer"

echo "👷 Add purchase_date field"
zrb project add fastapp field --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --column-name "purchase_date" --column-type "date"

echo "👷 Add available field"
zrb project add fastapp field --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --column-name "available" --column-type "boolean"

echo "👷 Add synopsis field"
zrb project add fastapp field --project-dir . --app-name "myapp" --module-name "library" \
    --entity-name "book" --column-name "synopsis" --column-type "text"

echo "👷 Start fastapp"
zrb project myapp monolith start
