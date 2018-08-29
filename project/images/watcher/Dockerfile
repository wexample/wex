FROM wexample/node:latest

COPY ./project/images/watcher/package.source.json /var/www/package.json
COPY ./project/images/watcher/entrypoint.sh /docker-entrypoint-watcher.sh
COPY ./project/images/watcher/gulpfile.js /var/www/gulpfile.js

# Install Gulp / Sass
RUN apt-get update && \
    apt-get install ruby-full -yqq && \
    gem install sass --no-user-install -q --no-verbose && \
    cd /var/www/ && \
    npm install -g gulp && \
    npm link gulp && \
    yarn install && \
    chmod +x /docker-entrypoint-watcher.sh

ENTRYPOINT ["/docker-entrypoint-watcher.sh"]
