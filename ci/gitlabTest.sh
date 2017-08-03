#!/bin/bash

# TODO We may use different images for each tests (drush && drupal / composer && Sympfony / etc...)

# Wexample loader for multiple scripts.
w=wexample.sh
curl -sS https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w

bash $w -s=gitlabInit -rm

# TEMP Install all project dependencies
php composer.phar clear-cache -q
php composer.phar update -q

# Run tests.
bash bash/ubuntu-16.x/tests/_run.sh

# Deploy to GitHub
bash $w -s=gitlabDeployGithub -a="git@github.com:wexample/scripts.git" -rm
