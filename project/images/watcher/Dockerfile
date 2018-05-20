FROM wexample/node:latest

# Gulp
RUN npm install --global gulp-cli
# Ruby
RUN apt-get install ruby-full -yqq
# Sass
RUN gem install sass --no-user-install -q --no-verbose

# Entrypoint
COPY ./project/images/watcher/entrypoint.sh /docker-entrypoint-watcher.sh
ENTRYPOINT ["/docker-entrypoint-watcher.sh"]
