FROM ubuntu:18.04

LABEL authors="Lionel Péramo <peramo.lionel@gmail.com>"

# Copy entrypoint.
COPY ./v2/images/ubuntu18/entrypoint.sh /docker-entrypoint-otra.sh

RUN export DEBIAN_FRONTEND=noninteractive && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get update && \
    apt-get install \
    apt-utils \
    cron \
    curl \
    git \
    gnupg2 \
    lsb-release \
    wget \
    tzdata \
    -yqq && \
    echo "Europe/Paris" > /etc/timezone && \
    rm /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    touch /var/default.cron && \
    chmod +x /docker-entrypoint-ubuntu18.sh && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-otra.sh"]
