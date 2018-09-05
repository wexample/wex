#!/usr/bin/env bash

frameworkSymfony4Install() {
# TODO Once sy4 will be detected,
#  wex frameworkComposer1/install

  wex site/exec -c="cd /var/www/html/project && npm install"
  # Test if webpack/encore is installed.
  if [ $(wex site/exec -c="wex file/exists -f=/var/www/html/project/node_modules/.bin/encore") == true ];then
    # Build assets.
    wex site/exec -c="cd /var/www/html/project && yarn run encore dev"
  fi
  # Fillup Symfony .env file with db URL
  . .wex
  wex config/setValue -f=./project/.env -k=DATABASE_URL -s="=" -v="mysql://root:${MYSQL_PASSWORD}@${NAME}_mysql:3306/${NAME}"
  # Set write.
  wex site/exec -c="chmod -R 755 /var/www/html/"
  wex site/exec -c="chown -R www-data:www-data /var/www/html/"
  # Fill doctrine database.
  wex site/exec -c="cd /var/www/html/project && php bin/console doctrine:schema:update --force"
  # Create an admin user
  wex site/exec -c="cd /var/www/html/project && php bin/console fos:user:create admin --super-admin"
}
