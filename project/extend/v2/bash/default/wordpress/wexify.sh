#!/usr/bin/env bash

wordpressWexifyArgs() {
  _DESCRIPTION="Convert an external wordpress site to a wex site. Warning ! Make a backup of your site"
  _ARGUMENTS=(
    [0]='database_dump db "Database SQL dump file" true'
  )
}

wordpressWexify() {

  # Invalid WP installation
  if [ ! -f "./wp-config.php" ];then
    echo "Missing ./wp-config.php file"
    return;
  fi

  . .wex

  local GOAL_VERSION=$(wex wordpress/version)
  local DB_PREFIX=$(wex wordpress/dbPrefix)
  local TEMP_FOLDER='../_bkp_'$(basename $(realpath ./))

  mkdir ${TEMP_FOLDER}
  # Hide move errors.
  $(mv {./*,./.*} ${TEMP_FOLDER}/) &> /dev/null
  # Init
  wex wexample::site/init -s=wordpress4,mysql,phpmyadmin

  echo 'WP_DB_TABLE_PREFIX='${DB_PREFIX} >> .wex
  echo 'WP_DEBUG_ENABLED=false' >> .wex

  # Copy content files
  cp -r ${TEMP_FOLDER}/wp-content/languages ./wordpress/public/
  cp -r ${TEMP_FOLDER}/wp-content/plugins ./wordpress/public/
  cp -r ${TEMP_FOLDER}/wp-content/themes ./wordpress/public/
  cp -r ${TEMP_FOLDER}/wp-content/uploads ./wordpress/public/

  if [ -d ${TEMP_FOLDER}/wp-content/backups ];then
    cp -r ${TEMP_FOLDER}/wp-content/backups ./wordpress/public/
  fi

  if [ -d ${TEMP_FOLDER}/wp-content/themes-child ];then
    cp -r ${TEMP_FOLDER}/wp-content/themes-child ./wordpress/public/
  fi

  cp ${DATABASE_DUMP} ./mysql/dumps
  local DUMP_FILE=$(basename ${DATABASE_DUMP})

  # Run website.
  wex site/start

  # Import database.
  wex db/restore -d=${DUMP_FILE}
  # Convert database.
  wex wordpress/urlChange -u='http://'${LOCAL_DOMAIN_MAIN}'/'
  wex db/anon

  # Set core to expected version.
  wex wordpress/changeCore -v=${GOAL_VERSION}

  # Trash old site.
  rm -rf ${TEMP_FOLDER}
}