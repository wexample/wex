#!/usr/bin/env bash

gitlabDeployGithub() {
  destRepoUrl=${1}
  
  # Add SSH and prevent host checking.
  apt-get install openssh-client -yqq

  mkdir -p ~/.ssh
  eval $(ssh-agent -s)
  [[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

  # Add ssh user.
  ssh-add <(echo "$STAGING_PRIVATE_KEY")

  # Install git.
  apt-get install git -yqq

  # Remove old repo first,
  # in case of previous fail.
  echo "Remove old repo"
  git remote remove github
  git remote add github "${destRepoUrl}"

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
