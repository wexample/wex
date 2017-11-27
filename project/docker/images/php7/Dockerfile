FROM wexample/webserver:latest

LABEL authors="wexample <contact@wexample.com>"

RUN apt-get update -yqq

# PHP
RUN apt-get install \
  php-memcache \
  php-memcached \
  memcached \
  php7.1 \
  libapache2-mod-php \
  php-gd \
  php-imagick \
  php-xml \
  php-mysql \
  mysql-client \
  -yqq

# Cleanup disk
RUN apt-get clean

# Composer install
RUN wex composer/pharInstall

COPY ./scripts/docker-entrypoint-php7.sh /

ENTRYPOINT ["/docker-entrypoint-php7.sh"]
