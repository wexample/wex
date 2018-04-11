#!/usr/bin/env bash

# The node_modules files in project must be installed from a container to have the right environment.
# We alos need to install node-sass manually in order to have the /vendore folder of gulp-sass filled
# ex : npm install node-sass@3.4.2

cd /var/www/html

gulp watch
