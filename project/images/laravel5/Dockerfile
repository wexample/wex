FROM wexample/php7:latest

COPY ./project/images/php7/entrypoint.sh /docker-entrypoint-laravel5.sh

# Add Yarn repository.
# Install NodeJS / NPM / Yarn / Xdebug.
# Configure npm.
# Cleanup.
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && \
    apt-get install \
    nodejs \
    npm \
    php-xdebug \
    yarn -yqq && \
    npm cache clean -f && \
    npm install -g n && \
    n latest && \
    chmod +x /docker-entrypoint-laravel5.sh && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-laravel5.sh"]
