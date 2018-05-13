#!/usr/bin/env bash

rocketchatInit() {

  # /!\ The Default used port of mongo should not be changed...

  local RENDER_BAR='wex render/progressBar -w=30 '

  # Still display progress bar.
  ${RENDER_BAR} -p=81 -s="Start mongo" -nl
  # This method is for info, we can perform several action on init.
  wex site/start -c=mongo

  ${RENDER_BAR} -p=82 -s="Wait 20 seconds for database fill.." -nl
  sleep 20

  . ./tmp/config

  # Create replica set
  docker exec ${SITE_NAME}_mongo mongo localhost:27017/rocketchat --eval "rs.initiate({ _id: \"rs0\", members: [ { _id: 0, host: \"localhost:27017\" } ]})"

  # Import default database
  # - admin / password
  # - hubot / pass given in yml file
  docker cp ${WEX_DIR_ROOT}docker/services/rocketchat/fixtures ${SITE_NAME}_mongo:/
  docker exec ${SITE_NAME}_mongo mongorestore --port 27017 /fixtures
  docker exec ${SITE_NAME}_mongo rm -rf /fixtures

  wex site/stop
}
