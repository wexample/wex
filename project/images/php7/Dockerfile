FROM wexample/webserver:latest

LABEL authors="wexample <contact@wexample.com>"

RUN apt-get update -yqq

# PHP
RUN apt-get install \
  php-memcache \
  php-memcached \
  php-zip \
  memcached \
  php7.1 \
  libapache2-mod-php \
  php-gd \
  php-imagick \
  php-xml \
  php-mysql \
  php-curl \
  mysql-client \
  -yqq

# Cleanup disk
RUN apt-get clean

# Composer install using wex.
RUN cd /opt/wexample/project/bash/ && bash wex composer/pharInstall

COPY ./project/images/php7/entrypoint.sh /docker-entrypoint-php7.sh
RUN chmod +x /docker-entrypoint-php7.sh

ENTRYPOINT ["/docker-entrypoint-php7.sh"]
