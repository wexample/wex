FROM ubuntu:20.04

LABEL authors="wexample <contact@wexample.com>"

# Copy entrypoint.
COPY ./v2/images/ubuntu18/entrypoint.sh /docker-entrypoint-ubuntu18.sh

# Configure non-interactivity.
# Install base packages.
# Adjust timezone.
# Init cron.
#   Create an empty cron file.
#   in case user does not provide it.
# Install wex scripts.
# Install entrypoint.
# Cleanup.
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
    tzdata \
    unzip \
    wget \
    zip \
    -yqq && \
    echo "Europe/Paris" > /etc/timezone && \
    rm /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    touch /var/default.cron && \
    chmod +x /docker-entrypoint-ubuntu18.sh && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-ubuntu18.sh"]
