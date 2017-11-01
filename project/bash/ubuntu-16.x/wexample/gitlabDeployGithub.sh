#!/usr/bin/env bash

wexampleGitlabDeployGithub() {
  # Init using wexample"s gitlab specific configuration.
  wex wexample/gitlabSshInit
  # Use normal gitlab to github deployment.
  wex gitlab/deployGithub "$@"
}
