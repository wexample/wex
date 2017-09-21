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

# Wexample loader for multiple scripts.
RUN wexample composerPharInstall -rm \
  # Install Symfony
  && wexample symfonyClientInstall -rm

COPY ./scripts/docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]
