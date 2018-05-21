FROM wexample/ubuntu17:latest

LABEL authors="wexample <contact@wexample.com>"

RUN apt-get update -yqq

# Web server
RUN apt-get install apache2 -yqq

# Add server name to prevent warnings
RUN sed -i "\$aServerName wexampleWebServer" /etc/apache2/apache2.conf

# Add VM user to www data (allow site modification)
RUN usermod -u 1000 www-data

# Activate apache2 mod rewrite.
RUN a2enmod rewrite
RUN a2enmod ssl

COPY ./project/images/webserver/entrypoint.sh /docker-entrypoint-webserver.sh
RUN chmod +x /docker-entrypoint-webserver.sh

ENTRYPOINT ["/docker-entrypoint-webserver.sh"]
