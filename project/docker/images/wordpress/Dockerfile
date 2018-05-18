FROM wordpress:4.9.5-apache

RUN apt-get update
RUN apt-get install nano -yqq

# Install WP CLI
RUN curl -o /wp-cli.phar -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
RUN chmod +x /wp-cli.phar
RUN mv /wp-cli.phar /usr/local/bin/wp

# Copy custom config that allow shared file config.
COPY ./project/docker/images/wordpress/wp-config.php /var/www/html/
RUN chown www-data:www-data /var/www/html/wp-config.php