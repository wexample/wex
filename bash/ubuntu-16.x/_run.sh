#!/usr/bin/env bash

# This method is used to execute any wexample script
# from an environment without wexample scripts installed.
s=helloWorld && f=wexample.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$f | tr -d '\015' > $f && bash $f -s=$s -rm -i
