FROM wexample/webserver:latest

LABEL authors="wexample <contact@wexample.com>"

COPY ./v2/images/php7/entrypoint.sh /docker-entrypoint-php7.sh

# Add PHP repository.
# Install packages.
# Install entrypoint.
# Cleanup.
RUN apt-get update -yqq && \
  apt-get install \
  software-properties-common -yqq && \
  add-apt-repository ppa:ondrej/php -y && \
  apt-get update -yqq && \
  apt-get install \
  libapache2-mod-php \
  memcached \
  mysql-client \
  nano \
  php-curl \
  php-gd \
  php-imagick \
  php-mbstring \
  php-memcache \
  php-memcached \
  php-mysql \
  php-xdebug \
  php-xml \
  php-zip \
  php7.3 \
  php7.3-apcu \
  php7.3-intl \
  sendmail \
  -yqq && \
  bash wex composer/pharInstall && \
  chmod +x /docker-entrypoint-php7.sh && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-php7.sh"]
