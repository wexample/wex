FROM wexample/php7:latest

LABEL authors="wexample <contact@wexample.com>"

COPY ./v2/images/php7/entrypoint.sh /docker-entrypoint-symfony4.sh

# Add Yarn repository.
# Install NodeJS / NPM / Yarn / Xdebug.
# Cleanup.
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
  && apt-get update \
  && curl -sL https://deb.nodesource.com/setup_12.x | bash - \
  && apt-get install \
  composer \
  nodejs \
  php-xdebug \
  yarn \
  -yq \
  && chmod +x /docker-entrypoint-symfony4.sh && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-symfony4.sh"]
