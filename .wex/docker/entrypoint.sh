#!/bin/bash

cd /var/www/html && pip install -r requirements.txt

exec "$@"
