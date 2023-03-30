#!/bin/bash

cd /opt/wex && pip install -r requirements.txt

exec "$@"
