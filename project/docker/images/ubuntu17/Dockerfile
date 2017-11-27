FROM ubuntu:17.10

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

ENV PATH="/opt/wexample/bash:${PATH}"

# Install wexample
RUN w=_install.sh \
 && curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w \
 && bash $w \
 && rm -rf $w

COPY ./scripts/docker-entrypoint-ubuntu17.sh /

ENTRYPOINT ["/docker-entrypoint-ubuntu17.sh"]

