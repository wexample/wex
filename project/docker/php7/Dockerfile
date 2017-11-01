FROM wexample/webserver:latest

LABEL authors="wexample <contact@wexample.com>"

RUN apt-get update -yqq

# PHP
RUN apt-get install \
  php-memcache \
  php-memcached \
  memcached \
  php \
  libapache2-mod-php \
  php-xml \
  php-mysql \
  mysql-client \
  yarn \
  -yqq

# Cleanup disk
RUN apt-get clean

# Update wexample
RUN wex wexample/update
# Composer install
RUN wex composer/pharInstall

COPY ./scripts/docker-entrypoint-php7.sh /

ENTRYPOINT ["/docker-entrypoint-php7.sh"]
