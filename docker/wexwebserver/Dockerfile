FROM weeger/wexubuntu16:latest

# Web server
RUN apt-get install apache2 -yqq

# Add server name to prevent warnings
RUN sed -i "\$aServerName localhost" /etc/apache2/apache2.conf

RUN usermod -u 1000 www-data

ENTRYPOINT /bin/bash
