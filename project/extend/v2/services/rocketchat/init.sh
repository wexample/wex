#!/usr/bin/env bash

rocketchatInit() {
  # Override default container.
  echo "ROCKETCHAT_VERSION=1.1.1" >> .wex

  echo "Fill default database."

  wex site/start -c=mongo

  . ./tmp/config

  # Create replica set
  docker exec ${SITE_NAME_INTERNAL}_mongo mongo localhost:27017/rocketchat --eval "rs.initiate({ _id: \"rs0\", members: [ { _id: 0, host: \"localhost:27017\" } ]})"

  # Import default database
  # - admin / password
  # - hubot / pass given in yml file
  docker cp ${WEX_DIR_SERVICES}rocketchat/fixtures ${SITE_NAME_INTERNAL}_mongo:/
  docker exec ${SITE_NAME_INTERNAL}_mongo mongorestore --port 27017 /fixtures
  docker exec ${SITE_NAME_INTERNAL}_mongo rm -rf /fixtures

  wex site/stop
}
