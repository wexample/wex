#!/usr/bin/env bash

# The node_modules files in project must be installed from a container to have the right environment.
# We also need to install node-sass manually in order to have the /vendor folder of gulp-sass filled
# ex : npm install -g node-sass@3.4.2

cd /var/www

gulp watch
