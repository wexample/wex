FROM ubuntu:18.04

LABEL authors="Lionel Péramo <peramo.lionel@gmail.com>"

# Copy entrypoint.
COPY ./v2/images/otra/entrypoint.sh /docker-entrypoint-otra.sh

RUN export DEBIAN_FRONTEND=noninteractive && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt install software-properties-common && \
    add-apt-repository ppa:ondrej/php && \
    apt update && \
    apt install \
    cron \
    curl \
    git \
#    php7.4-curl \
#    php7.4-mbstring \
#    php7.4-mysql \
#    php7.4-xml \
    -yqq && \
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php -r "if (hash_file('sha384', 'composer-setup.php') === 'a5c698ffe4b8e849a443b120cd5ba38043260d5c4023dbf93e1558871f1f07f58274fc6f4c93bcfd858c6bd0775cd8d1') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" && \
    php composer-setup.php && \
    php -r "unlink('composer-setup.php');" && \
    echo "Europe/Paris" > /etc/timezone && \
    rm /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    touch /var/default.cron && \
    chmod +x /docker-entrypoint-otra.sh && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/docker-entrypoint-otra.sh"]
