FROM wexample/node:latest

# Ruby
RUN apt-get install ruby-full -yqq
# Sass
RUN gem install sass --no-user-install -q --no-verbose
# Node modules

COPY ./project/images/watcher/package.source.json /var/www/package.json
RUN cd /var/www/ && npm install
RUN npm install -g gulp

COPY ./project/images/watcher/gulpfile.js /var/www/gulpfile.js

# Entrypoint
COPY ./project/images/watcher/entrypoint.sh /docker-entrypoint-watcher.sh
RUN chmod +x /docker-entrypoint-watcher.sh

ENTRYPOINT ["/docker-entrypoint-watcher.sh"]
