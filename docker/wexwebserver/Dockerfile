FROM wexample/wexubuntu16:latest

# Web server
RUN apt-get install apache2 -yqq

# Add server name to prevent warnings
RUN sed -i "\$aServerName localhost" /etc/apache2/apache2.conf

# Add VM user to www data (allow site modification)
RUN usermod -u 1000 www-data

# Activate apache2 mod rewrite.
RUN a2enmod rewrite

ENTRYPOINT /bin/bash
