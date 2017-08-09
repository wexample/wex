FROM wexample/wexwebserver:latest

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
RUN w=wexample.sh && curl -sS https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w \
  # Install composer
  && bash $w -s=composerPharInstall -rm \
  # Install Symfony
  && bash $w -s=symfonyClientInstall -rm

COPY ./scripts/docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]
