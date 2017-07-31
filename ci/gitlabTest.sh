#!/bin/bash

# Wexample loader for multiple scripts.
w=wexample.sh
curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w -s | tr -d '\015' > $w

# Remove warning on new SSH host.
bash $w -s=gitlabInit -rm
bash $w -s=gitlabInstallComposer -rm

# Run tests.
bash bash/ubuntu-16.x/tests/_run.sh

# Deploy to GitHub
bash $w -s=gitlabDeployGithub -a="git@github.com:wexample/scripts.git" -rm
