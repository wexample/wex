FROM wexample/php7:latest

ENV WORDPRESS_VERSION 4.9.5

ADD https://wordpress.org/wordpress-${WORDPRESS_VERSION}.tar.gz /wordpress.tar.gz
ADD https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar /wp-cli.phar

RUN apt-get update && \
    apt-get install \
    wget \
    zip \
    -yq && \
    tar -xzf wordpress.tar.gz -C /var/www/html/ && \
    mv /var/www/html/wordpress /var/www/html/project && \
	  rm wordpress.tar.gz && \
	  chown -R www-data:www-data /var/www/html/project && \
	  chmod +x /wp-cli.phar && \
    mv /wp-cli.phar /usr/local/bin/wp

# Copy custom config that allow shared file config.
COPY ./project/images/wordpress4/wp-config.php /var/www/html/project

RUN chown www-data:www-data /var/www/html/project/wp-config.php