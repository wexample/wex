FROM wexample/wexwebserver:latest

RUN apt-get update

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
  -yqq

# Cleanup disk
RUN apt-get clean

# Update wexample
RUN wex wexample/update
# Wexample loader for multiple scripts.
RUN wex composer/pharInstall
# Install Symfony
RUN wex frameworkSymfony3/clientInstall

COPY ./scripts/docker-entrypoint-wexphp7.sh /

ENTRYPOINT ["/docker-entrypoint-wexphp7.sh"]
