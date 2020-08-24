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
  php7.3 \
  php7.3-apcu \
  php7.3-curl \
  php7.3-gd \
  php7.3-imagick \
  php7.3-intl \
  php7.3-mbstring \
  php7.3-memcache \
  php7.3-memcached \
  php7.3-mysql \
  php7.3-xdebug \
  php7.3-xml \
  php7.3-zip \
  sendmail \
  -yqq && \
  a2dismod php7.4 && \
  a2enmod php7.3 && \
  service apache2 restart && \
  php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
  php -r "if (hash_file('sha384', 'composer-setup.php') === '8a6138e2a05a8c28539c9f0fb361159823655d7ad2deecb371b04a83966c61223adc522b0189079e3e9e277cd72b8897') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" && \
  php composer-setup.php && \
  php -r "unlink('composer-setup.php');" && \
  chmod +x /docker-entrypoint-php7.sh && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-php7.sh"]
