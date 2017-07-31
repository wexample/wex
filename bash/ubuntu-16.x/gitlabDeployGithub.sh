#!/usr/bin/env bash

gitlabDeployGithub() {
  destRepoUrl=${1}

  # Add git repo.
  echo "Remove repo (old)"
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
  echo "Pull / Push"
  git pull github master
  git push github master
  echo "Remove repo"
  git remote remove github
  git remote add github "${destRepoUrl}"
}
