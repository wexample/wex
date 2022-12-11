FROM ubuntu:14.04

LABEL authors="wexample <contact@wexample.com>"

ENV PATH="/opt/wexample/project/bash:${PATH}"

# Install wex scripts.
COPY ./ /opt/wexample/
# Install entrypoint.
COPY ./v2/images/ubuntu16/entrypoint.sh /docker-entrypoint-ubuntu14.sh

RUN apt-get update && \
  apt-get install \
  realpath \
  file \
  curl \
  git \
  nano \
  net-tools \
  wget \
  zip unzip \
  zlib1g-dev \
  -yqq && \
  bash /opt/wexample/project/bash/default/_installLocal.sh && \
  chmod +x /docker-entrypoint-ubuntu14.sh

ENTRYPOINT ["/docker-entrypoint-ubuntu14.sh"]

