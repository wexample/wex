#!/bin/bash

sudo apt-get update
sudo apt-get install phpmyadmin php-mbstring php-gettext

# > select apache2
# > set yes for dbconfig-common

sudo phpenmod mcrypt
sudo phpenmod mbstring

# Create symlink to phpmyadmin conf
sudo ln -s  /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
# Enable symlink with another symlink
sudo ln -s /etc/apache2/conf-available/phpmyadmin.conf /etc/apache2/conf-enabled/phpmyadmin.conf

service apache2 restart
