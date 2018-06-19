FROM wexample/php7:latest

RUN apt-get install php-intl php-xmlrpc php-soap -yqq

# Cleanup dir
RUN mkdir /var/www/html/project && \
    cd /var/www/html/project && \
    git clone -b MOODLE_35_STABLE git://git.moodle.org/moodle.git --depth=1 .

# Manage access
RUN cd /var/www/html && chown -R root project && chmod -R 0755 project && find project -type f -exec chmod 0644 {} \; && \
    mkdir /var/www/html/moodledata && \
    chown www-data:www-data /var/www/html/moodledata && \
    chmod 755 /var/www/html/moodledata

# Enable SSL, moodle requires it
RUN a2enmod ssl && a2ensite default-ssl && service apache2 restart

# Copy custom config that allow shared file config.
COPY ./project/images/moodle/config.php /var/www/html/project/config.php