#!/usr/bin/env bash

# This method is used to execute any wexample script
# from an environment without wexample scripts installed.
s=helloWorld && w=wex && curl https://raw.githubusercontent.com/wexample/scripts/master/project/bash/$w | tr -d '\015' > $w && bash $w -s=$s -rm && rm -rf $w

# Wexample loader for multiple scripts.
w=wex
curl https://raw.githubusercontent.com/wexample/scripts/master/bash/$w | tr -d '\015' > $w
bash $w -s=helloWorld -rm
bash $w -s=helloWorld -rm
# Etc...
rm -rf $w
