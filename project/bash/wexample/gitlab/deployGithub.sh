#!/usr/bin/env bash

gitlabDeployGithub() {
  # Init using wexample"s gitlab specific configuration.
  wex wexample::gitlab/sshInit
  # Use normal gitlab to github deployment.
  wex gitlab/deployGithub "$@"
}
