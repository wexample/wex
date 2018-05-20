FROM wexample/php7:latest

ENV WORDPRESS_VERSION 4.9.5

RUN curl -o wordpress.tar.gz -O https://wordpress.org/wordpress-${WORDPRESS_VERSION}.tar.gz;
RUN tar -xzf wordpress.tar.gz -C /var/www/html/; \
    mv /var/www/html/wordpress /var/www/html/project; \
	rm wordpress.tar.gz; \
	chown -R www-data:www-data /var/www/html/project

# Install WP CLI
RUN curl -o /wp-cli.phar -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
RUN chmod +x /wp-cli.phar
RUN mv /wp-cli.phar /usr/local/bin/wp

# Copy custom config that allow shared file config.
COPY ./project/docker/images/wordpress/wp-config.php /var/www/html/project
RUN chown www-data:www-data /var/www/html/project/wp-config.php