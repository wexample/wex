FROM wordpress:4.9.5-apache

# Install WP CLI
RUN curl -o /wp-cli.phar -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
RUN chmod +x /wp-cli.phar
RUN mv /wp-cli.phar /usr/local/bin/wp
RUN wp --info
