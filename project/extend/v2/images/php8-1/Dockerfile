FROM wexample/webserver:latest

LABEL authors="wexample <contact@wexample.com>"

COPY ./v2/images/php8/entrypoint.sh /docker-entrypoint-php8.sh

# Add PHP repository.
# Install packages.
# Install entrypoint.
# Cleanup.
RUN apt-get update -yqq && \
  c \
  software-properties-common -yqq && \
  add-apt-repository ppa:ondrej/php -y && \
  apt-get update -yqq && \
  apt-get install \
  composer \
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
  php8.1 \
  php8.1-fpm \
  php8.1-intl \
  sendmail \
  -yqq && \
  chmod +x /docker-entrypoint-php8.sh && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-php8.sh"]
