#!/usr/bin/env bash

# This method is used to execute any wexample script
# from an environment without wexample scripts installed.
s=helloWorld && w=wexample.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w && bash $w -s=$s -i -rm && rm -rf $w

# Same script for multiple sub scripts
w=wexample.sh
curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w
bash $w -s=helloWorld -rm
bash $w -s=helloWorld -rm
# Etc...
rm -rf $w
