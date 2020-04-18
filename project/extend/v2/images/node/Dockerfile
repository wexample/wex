FROM wexample/ubuntu18:latest

LABEL authors="wexample <contact@wexample.com>"

# Copy wex scripts
COPY ./ /opt/wexample/
# Copy entrypoint.
COPY ./v2/images/node/entrypoint.sh /docker-entrypoint-node.sh

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
  apt-get update && \
  -sL https://deb.nodesource.com/setup_12.x | -E bash - && \
  apt-get install \
  nano \
  nginx \
  nodejs \
  npm \
  yarn \
  -yqq && \
  chmod +x /docker-entrypoint-node.sh && \
  /etc/init.d/nginx start

ENTRYPOINT ["/docker-entrypoint-node.sh"]
