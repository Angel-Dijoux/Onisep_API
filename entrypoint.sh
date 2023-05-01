#! /bin/bash 

sleep 120
if [ ! -d "/app/migrations" ]; then
  echo "Init database"
  flask db init
fi
echo "Run migration"
flask db migrate -m 'create initial tables'
echo "Upgrade tables"
flask db upgrade
echo "Finish"

exec "$@"