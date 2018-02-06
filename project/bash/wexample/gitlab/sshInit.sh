#!/usr/bin/env bash

gitlabSshInit() {
  if [ -z "${STAGING_PRIVATE_KEY+x}" ]; then
    echo "Missing secret CI variable STAGING_PRIVATE_KEY"
    exit 1
  fi;

  # Save deployment key,
  # we can't pass key by argument directly,
  # the key is not recognized, maybe quotes or line ending issue,
  # so we use a local file.
  DEPLOY_KEY="/deployKey"

  # The variable name is set into project variables settings.
  echo "${STAGING_PRIVATE_KEY}" > ${DEPLOY_KEY};
  # SSH expect restricted access
  chmod 400 ${DEPLOY_KEY}

  wex ubuntu-16.x::gitlab/sshInit -k=${DEPLOY_KEY}
}
