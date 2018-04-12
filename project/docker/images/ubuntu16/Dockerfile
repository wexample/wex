FROM ubuntu:16.04

LABEL authors="wexample <contact@wexample.com>"

RUN apt-get update -yqq

# Utils
RUN apt-get install \
  file \
  curl \
  git \
  nano \
  net-tools \
  wget \
  zip unzip \
  zlib1g-dev \
  -yqq

ENV PATH="/opt/wexample/project/bash:${PATH}"

# Install wex scripts.
COPY ./ /opt/wexample/
RUN bash /opt/wexample/project/bash/ubuntu-16.x/_installLocal.sh

# Install entrypoint.
COPY ./project/docker/images/ubuntu16/entrypoint.sh /docker-entrypoint-ubuntu16.sh
ENTRYPOINT ["/docker-entrypoint-ubuntu16.sh"]

