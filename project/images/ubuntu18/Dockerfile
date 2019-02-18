FROM ubuntu:18.04

LABEL authors="wexample <contact@wexample.com>"

# Copy wex scripts
COPY ./ /opt/wexample/
# Copy entrypoint.
COPY ./project/images/ubuntu18/entrypoint.sh /docker-entrypoint-ubuntu18.sh

# Adjust timezone
# Init cron
#   Create an empty cront file
#   in case user does not provide it.
# Install wex scripts.
# Install entrypoint.

RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install cron apt-utils gnupg2 tzdata git -yqq && \
    echo "Europe/Paris" > /etc/timezone && \
    rm /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    touch /var/default.cron && \
    bash /opt/wexample/project/bash/default/_installLocal.sh && \
    chmod +x /docker-entrypoint-ubuntu18.sh

ENTRYPOINT ["/docker-entrypoint-ubuntu18.sh"]
