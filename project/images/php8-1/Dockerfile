FROM wexample/webserver:latest

LABEL authors="wexample <contact@wexample.com>"

COPY ./v2/images/php8/entrypoint.sh /docker-entrypoint-php8.sh

RUN apt-get update -yqq && \
  apt-get install \
  software-properties-common -yqq && \
  add-apt-repository ppa:ondrej/php -y && \
  apt-get update -yqq && \
  apt-get install \
  composer \
  curl \
  libapache2-mod-php \
  memcached \
  mysql-client \
  nano \
  php8.1 \
  php8.1-curl \
  php8.1-fpm \
  php8.1-gd \
  php8.1-imagick \
  php8.1-mbstring \
  php8.1-memcache \
  php8.1-memcached \
  php8.1-mysql \
  php8.1-xml \
  php8.1-zip \
  php8.1-intl \
  sendmail \
  unzip \
  zip \
  -yqq \
  && a2enmod proxy_fcgi setenvif \
  && a2enconf php8.1-fpm \
  && chmod +x /docker-entrypoint-php8.sh \
  && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-php8.sh"]
