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
  php-zip \
  php7.3 \
  php7.3-apcu \
  php7.3-intl \
  php7.3-xml \
  sendmail \
  -yqq && \
  php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
  php -r "if (hash_file('sha384', 'composer-setup.php') === 'e5325b19b381bfd88ce90a5ddb7823406b2a38cff6bb704b0acc289a09c8128d4a8ce2bbafcd1fcbdc38666422fe2806') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" && \
  php composer-setup.php && \
  php -r "unlink('composer-setup.php');" && \
  chmod +x /docker-entrypoint-php7.sh && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-php7.sh"]
