#!/usr/bin/env bash

rocketchatInit() {
  echo "Fill default database."

  wex site/start -c=mongo

  . ./tmp/config

  # Create replica set
  docker exec ${SITE_NAME}_mongo mongo localhost:27017/rocketchat --eval "rs.initiate({ _id: \"rs0\", members: [ { _id: 0, host: \"localhost:27017\" } ]})"

  # Import default database
  # - admin / password
  # - hubot / pass given in yml file
  docker cp ${WEX_DIR_ROOT}services/rocketchat/fixtures ${SITE_NAME}_mongo:/
  docker exec ${SITE_NAME}_mongo mongorestore --port 27017 /fixtures
  docker exec ${SITE_NAME}_mongo rm -rf /fixtures

  wex site/stop
}
