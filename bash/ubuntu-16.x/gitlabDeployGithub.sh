#!/usr/bin/env bash

gitlabDeployGithub() {
  destRepoUrl=${1}

  # Add git repo.
  git remote remove github
  git remote add github "${destRepoUrl}"
  # Remove branch if exists.
  git branch -d temp
  # Use temp branch to attach head.
  git branch temp
  git checkout temp
  git branch -f master temp
  git checkout master
  # Get last updates on git repo.
  git pull github master
  # Push on git repo.
  git push github master
}
