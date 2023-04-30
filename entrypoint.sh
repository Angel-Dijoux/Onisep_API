#! /bin/bash 

flask db init
flask db migrate -m 'create initial tables'
flask db upgrade
