#!/usr/bin/env bash

gitlabDeployGithubArgs() {
  _ARGUMENTS=(
    [0]='repo r "Github repository address" true'
    [1]='private_key_file k "Private key stored into project variables" true'
  )
}

gitlabDeployGithub() {
  wex gitlab/sshInit -k=${PRIVATE_KEY_FILE}

  # Install git.
  apt-get install git -yqq

  # Remove old repo first,
  # in case of previous fail.
  echo "Remove old repo"
  git remote remove github
  git remote add github "${REPO}"

  echo "Create temp branch and checkout"
  # Remove branch if exists.
  git branch -d temp
  # Use temp branch to attach head.
  git branch temp
  git checkout temp

  echo "Merge with master"
  git branch -f master temp

  echo "Go to master"
  git checkout master

  # Push on git repo.
  echo "Push"
  git push github master
}
