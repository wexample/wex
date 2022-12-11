FROM wexample/php7:latest

# Install Drush && Drupal
RUN git clone https://github.com/drush-ops/drush.git /usr/local/src/drush && \
    cd /usr/local/src/drush && \
    git checkout 8.1.17 && \
    ln -s /usr/local/src/drush/drush /usr/bin/drush && \
    composer install && \
    drush --version && \
    cd /var/www/html && \
    drush dl drupal-7.x && \
    mv drupal-7.x-dev project && \
    chown -R www-data:www-data project
