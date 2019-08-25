FROM wexample/ubuntu18:latest

LABEL authors="wexample <contact@wexample.com>"

# Copy wex scripts
COPY ./ /opt/wexample/
# Copy entrypoint.
COPY ./project/images/node/entrypoint.sh /docker-entrypoint-node.sh

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
  apt-get update && \
  apt-get install \
  nodejs \
  npm \
  yarn \
  -yqq

ENTRYPOINT ["/docker-entrypoint-node.sh"]
