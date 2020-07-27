#!/usr/bin/env bash

mysqlAppConfig() {
    # TODO Force using v3. Remove after services migration.
  unset -f wex

  . .wex

  local ACCESS=($(mysqlAppConfigAccess))

  wex config/addTitle -t="MySql"

  wex config/bindFiles -s=mysql -e=cnf

  wex config/setValue -k=MYSQL_DB_HOST -v=${ACCESS[0]}
  wex config/setValue -k=MYSQL_DB_PORT -v=${ACCESS[1]}
  wex config/setValue -k=MYSQL_DB_NAME -v=${ACCESS[2]}
  wex config/setValue -k=MYSQL_DB_USER -v=${ACCESS[3]}
  wex config/setValue -k=MYSQL_DB_PASSWORD -v=${ACCESS[4]}

  # Connexion file.
  local DB_CONNECTION_FILE=./tmp/mysql.cnf
  _wexLog "Creates connexion file info in ${DB_CONNECTION_FILE}"

  chmod 755 ${DB_CONNECTION_FILE}
  echo '[client]' > ${DB_CONNECTION_FILE}
  wex config/setValue -k=host -v=${ACCESS[0]} -f=${DB_CONNECTION_FILE}
  wex config/setValue -k=user -v=${ACCESS[3]} -f=${DB_CONNECTION_FILE}
  wex config/setValue -k=password -v=${ACCESS[4]} -f=${DB_CONNECTION_FILE}

  # Expected access level
  chmod 644 ${DB_CONNECTION_FILE}
}

mysqlAppConfigAccess() {
  local MYSQL_PASSWORD='thisIsAReallyNotSecurePassword!'

  . .wex

  # Host
  echo ${NAME}_$(wex site/env)_mysql
  # Port
  echo 3306
  # Name
  echo ${NAME}
  # User
  echo root
  # Password
  echo "${MYSQL_PASSWORD}"
}