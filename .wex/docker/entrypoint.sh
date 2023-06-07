#!/bin/bash

cd /opt/wex

pip install -r requirements.txt

. .wex/.env

ln -s /opt/wex "/var/www/${APP_ENV}/wex"

exec "$@"
