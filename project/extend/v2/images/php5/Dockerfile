FROM wexample/ubuntu14:latest

LABEL authors="wexample <contact@wexample.com>"

COPY ./v2/images/php5/entrypoint.sh /docker-entrypoint-php5.sh

RUN apt-get update -yqq && \
    apt-get install apache2 \
    php5 \
    php5-gd \
    php5-imagick \
    php5-memcached \
    php5-mysql \
    php5-curl \
    memcached \
    mysql-client \
    -yqq && \
    a2enmod rewrite && \
    a2enmod ssl && \
    a2enmod headers && \
    apt-get clean && \
    cd /opt/wexample/project/bash/ && \
    bash wex composer/pharInstall && \
    chmod +x /docker-entrypoint-php5.sh && \
    sed -i "\$aServerName wexampleWebServer" /etc/apache2/apache2.conf && \
    usermod -u 1000 www-data \
    && service apache2 restart

ENTRYPOINT ["/docker-entrypoint-php5.sh"]
