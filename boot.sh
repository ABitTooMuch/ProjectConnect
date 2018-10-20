#!/bin/sh
# Docker boot script
source venv/bin/activate

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deployment failed
    sleep 5
done
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - projectconnect:app