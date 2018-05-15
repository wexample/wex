#!/usr/bin/env bash

gitlabSshInit() {
  # Gitlab runner configuration must have a shared folder
  # declared into /etc/gitlab-runner/config.toml
  # volumes = [ ... ,"/root/.ssh:/root/.ssh/host/"]
  # It allow deployment system to use server rsa key pair for deployment.
  local DEPLOY_KEY="/root/.ssh/host/id_rsa"

  # The variable name is set into project variables settings.
  echo "${STAGING_PRIVATE_KEY}" > ${DEPLOY_KEY};
  # SSH expect restricted access
  chmod 400 ${DEPLOY_KEY}

  wex default::gitlab/sshInit -k=${DEPLOY_KEY}
}
