FROM wexample/php8:latest

LABEL authors="wexample <contact@wexample.com>"

COPY ./v2/images/symfony5/entrypoint.sh /docker-entrypoint-symfony5.sh

# Add Yarn repository.
# Install NodeJS / NPM / Yarn / Xdebug / Composer
# Configure CGI for PHP FPM
# Install symfony cli
# Cleanup.
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
  && apt-get update \
  && apt-get install \
  nodejs \
  php-xdebug \
  yarn \
  -yq \
  && wget https://raw.githubusercontent.com/composer/getcomposer.org/76a7060ccb93902cd7576b67264ad91c8a2700e2/web/installer -O - -q | php -- --quiet \
  && mv composer.phar /usr/local/bin/composer \
  && a2enmod alias proxy_fcgi \
  && wget https://get.symfony.com/cli/installer -O - | bash \
  && mv /root/.symfony/bin/symfony /usr/local/bin/symfony \
  && chmod +x /docker-entrypoint-symfony5.sh \
  && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-symfony5.sh"]
