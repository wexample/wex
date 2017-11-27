#!/usr/bin/env bash

gitlabSshInit() {
  # Save deployment key,
  # we can't pass key by argument directly,
  # the key is not recognized, maybe quotes or line ending issue,
  # so we use a local file.
  DEPLOY_KEY="/deployKey"

  # The variable name is set into project variables settings.
  echo "${STAGING_PRIVATE_KEY}" > ${DEPLOY_KEY};
  # SSH expect restricted access
  chmod 400 ${DEPLOY_KEY}

  wex gitlab/sshInit -k=${DEPLOY_KEY}
}
