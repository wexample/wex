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

ENV PATH="/opt/wexample/project/bash:${PATH}"

# TODO : set wex scripts version (tag)
# Install wexample
RUN v=w=_install.sh \
 && curl https://raw.githubusercontent.com/wexample/scripts/master/project/bash/ubuntu-16.x/$w | tr -d '\015' > $w \
 && bash $w \
 && rm -rf $w

COPY ./scripts/docker-entrypoint-ubuntu16.sh /

ENTRYPOINT ["/docker-entrypoint-ubuntu16.sh"]

