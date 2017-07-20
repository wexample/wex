#!/usr/bin/env bash

# TODO TEMP used for now just to save and construct shorthand function
s=wordpressMigrateDatabase.sh && f=wexampleLoader.sh && curl http://gitlab.wexample.com/wexample-public/scripts/raw/master/shell/ubuntu-16.x/$f | tr -d '\015' > $f && sudo bash $f $s && sudo rm -rf $f

