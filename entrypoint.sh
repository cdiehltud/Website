#!/bin/bash

COUCHDB_STATUS=0
while [ $COUCHDB_STATUS -ne 200 ];
do
  echo "CouchDB not available yet"
  COUCHDB_STATUS=$(
      curl "$EA_COUCHDB_URL/" \
          --write-out %{http_code} \
          --silent --output /dev/null)
  sleep 1
done

DATABASE_STATUS=$(
    curl "$EA_COUCHDB_URL/$EA_COUCHDB_NAME" \
        --write-out %{http_code} \
        --silent --output /dev/null)

if [ "$DATABASE_STATUS" -ne "200" ];
then
  echo "create database and import data"
  /app/couchdb-backup.sh -r -c \
    -H db -d $EA_COUCHDB_NAME -f /app/initial-data.json
fi

python $@
