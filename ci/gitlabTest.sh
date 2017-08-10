#!/bin/bash

# TODO We may use different images for each tests (drush && drupal / composer && Symfony / etc...)

# Wexample loader for multiple scripts.
w=wexample.sh
curl -sS https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w

bash $w -s=gitlabInit -rm

bash $w -s=composerUpdate -rm

# Run tests.
bash bash/ubuntu-16.x/tests/_run.sh

# Deploy to GitHub
bash $w gitlabDeployGithub "git@github.com:wexample/scripts.git" -rm
