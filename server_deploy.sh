#!/bin/bash

git pull
source .venv/bin/activate
pipenv install
cd cz3002_backend/
python3 manage.py test
python3 manage.py migrate
ps axf|grep "manage.py"|grep -v grep| awk '{print "kill -9 " $1}'|sh
nohup ./manage.py runserver 0:80 > nohup.out 2>&1 &

echo "Done deploy"