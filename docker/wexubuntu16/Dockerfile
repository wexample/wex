FROM ubuntu:16.04

LABEL authors="wexample <contact@wexample.com>"

RUN apt-get update -yqq

# Utils
RUN apt-get install \
  curl \
  git \
  nano \
  net-tools \
  wget \
  zip unzip \
  zlib1g-dev \
  -yqq

ENV PATH="/opt/wexample/bash:${PATH}"

# Install wexample
RUN w=_install.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w && bash $w && rm -rf $w
