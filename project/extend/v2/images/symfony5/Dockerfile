FROM wexample/php8-1:latest

LABEL authors="wexample <contact@wexample.com>"

COPY ./v2/images/symfony5/entrypoint.sh /docker-entrypoint-symfony5.sh

# Add Yarn repository.
# Install NodeJS / NPM / Yarn
# Install symfony cli
# Cleanup.
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
  && apt-get update \
  && apt-get install -yq \
  nodejs \
  npm \
  php8.1-bcmath \
  yarn \
  && a2enmod alias proxy_fcgi \
  && wget https://get.symfony.com/cli/installer -O - | bash \
  && mv /root/.symfony/bin/symfony /usr/local/bin/symfony \
  && chmod +x /docker-entrypoint-symfony5.sh \
  && rm -rf /var/lib/apt/lists/* \
  && npm install n -g \
  && n stable \
  && php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" \
  && php composer-setup.php \
  && mv composer.phar /usr/local/bin/composer \
  && service php8.1-fpm start

ENTRYPOINT ["/docker-entrypoint-symfony5.sh"]
