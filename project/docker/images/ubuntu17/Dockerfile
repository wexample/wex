FROM ubuntu:17.10

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
  php-mbstring \
  locales \
  cron \
  dos2unix \
  -yqq

# Adjust timezone
RUN export DEBIAN_FRONTEND=noninteractive && apt-get install tzdata -yqq
RUN echo "Europe/Paris" > /etc/timezone
RUN rm /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Init cron
# Create an empty cront file
# in case user does not provide it.
RUN touch /var/default.cron

ENV PATH="/opt/wexample/project/bash:${PATH}"

# Install wex scripts.
COPY ./ /opt/wexample/
RUN bash /opt/wexample/project/bash/ubuntu-16.x/_installLocal.sh

# Install entrypoint.
COPY ./project/docker/images/ubuntu17/entrypoint.sh /docker-entrypoint-ubuntu17.sh
ENTRYPOINT ["/docker-entrypoint-ubuntu17.sh"]

