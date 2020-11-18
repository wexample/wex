#!/usr/bin/env bash

gitlabSshInit() {
  # Gitlab runner configuration must have a shared folder
  # declared into /etc/gitlab-runner/config.toml
  # volumes = [ ... ,"/root/.ssh:/root/.ssh/host/"]
  # It allow deployment system to use server rsa key pair for deployment.
  wex default::gitlab/sshInit -k="/root/.ssh/host/id_rsa"
}
