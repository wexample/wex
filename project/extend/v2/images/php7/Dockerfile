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
  php-cli \
  php-curl \
  php-common \
  php-dev \
  php-fpm \
  php-gd \
  php-imagick \
  php-mbstring \
  php-memcache \
  php-memcached \
  php-mysql \
  php-xdebug \
  php-xml \
  php-zip \
  php-apcu \
  php-intl \
  sendmail \
  -yqq && \
  php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
  php -r "if (hash_file('sha384', 'composer-setup.php') === '756890a4488ce9024fc62c56153228907f1545c228516cbf63f885e036d37e9a59d27d63f46af1d4d07ee0f76181c7d3') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" && \
  php composer-setup.php && \
  php -r "unlink('composer-setup.php');" && \
  chmod +x /docker-entrypoint-php7.sh && \
  rm -rf /var/lib/apt/lists/* && \
  a2enmod proxy_fcgi

ENTRYPOINT ["/docker-entrypoint-php7.sh"]
