FROM wordpress:5.6.1-php7.4-apache

RUN apt-get update && \
    apt-get install \
    nano \
    sudo \
    -yq && \
    a2enmod expires && \
    a2enmod ext_filter && \
    docker-php-ext-install pdo_mysql && \
    apt-get clean