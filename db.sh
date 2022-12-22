#!/bin/sh

# drop, create, migrate schema of a given database
migratedb () {
    export DJANGO_SETTINGS_MODULE=myproject.settings.test
    dropdb test_db
    createdb test_db
    ./manage.py migrate
}

# create a backup of a given database
backupdb () {
    if [ $# -eq 0 ]
    then
        echo "db_name not specified"
    else
        db_name=$1
        db_name_copy=${db_name}_copy
        psql -c "DROP DATABASE $db_name_copy;"
        psql -c "CREATE DATABASE $db_name_copy WITH TEMPLATE $db_name;"
    fi
}

# restore database from a given backup
restoredb () {
    if [ $# -eq 0 ]
    then
        echo "db_name not specified"
    else
        db_name=$1
        db_name_copy=${db_name}_copy
        psql -c "DROP DATABASE $db_name;"
        psql -c "CREATE DATABASE $db_name WITH TEMPLATE $db_name_copy;"
    fi
}
