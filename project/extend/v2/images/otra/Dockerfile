FROM ubuntu:18.04

LABEL authors="Lionel Péramo <peramo.lionel@gmail.com>"

# Copy entrypoint.
COPY ./v2/images/otra/entrypoint.sh /docker-entrypoint-otra.sh

# apt-utils in installed in order to remove the future messages like this
# "debconf: delaying package configuration, since apt-utils is not installed"
RUN export DEBIAN_FRONTEND=noninteractive && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get update -yqq && \
    apt-get install -yqq \
    apt-utils \
    software-properties-common && \
    add-apt-repository ppa:ondrej/php -y && \
    apt-get install apache2 -yqq && \
    usermod -u 1000 www-data && \
    a2enmod rewrite && \
    a2enmod ssl && \
    a2enmod headers && \
    a2enmod expires && \
    apt-get install -yqq \
    vim \
    cron \
    curl \
    git \
    tzdata \
    php7.4 \
    php7.4-curl \
    php7.4-mbstring \
    php7.4-mysql \
    php7.4-xml && \
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php -r "if (hash_file('sha384', 'composer-setup.php') === 'e0012edf3e80b6978849f5eff0d4b4e4c79ff1609dd1e613307e16318854d24ae64f26d17af3ef0bf7cfb710ca74755a') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" && \
    php composer-setup.php && \
    php -r "unlink('composer-setup.php');" && \
    echo "Europe/Paris" > /etc/timezone && \
    rm /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    touch /var/default.cron && \
    chmod +x /docker-entrypoint-otra.sh && \
    rm -rf /var/lib/apt/lists/* && \
    echo \"alias composer=php composer.phar\" >> ~/.bashrc

ENTRYPOINT ["/docker-entrypoint-otra.sh"]
