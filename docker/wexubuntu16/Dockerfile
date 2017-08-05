FROM ubuntu:16.04

LABEL authors="wexample <contact@wexample.com>"

RUN apt-get update -yqq

# Utils
RUN apt-get install nano curl git wget zip unzip zlib1g-dev -yqq

# Install wexample utils
RUN w=_install.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w && . $w && rm -rf $w
