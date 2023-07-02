#! /bin/bash 

sleep 75
if [ ! -d "/app/migrations" ]; then
  echo "Init database"
  flask db init
fi
echo "Upgrade tables"
flask db upgrade
echo "Finish"

exec "$@"