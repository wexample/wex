#!/bin/bash

wexRelease() {
  # Go to wexample install dir.
  cd ${WEX_DIR_ROOT}../

  # Reset.
  wex git/resetHard
  # Pull last version.
  git pull origin master

  # Generate a version.
  VERSION=$(wex version/generate -v=2)

  # Add tag if not exists.
  echo "Tagging at version "${VERSION}
  if [ $(wex git/tagExists -t=${VERSION}) == false ];then
    # Create a tag.
    git tag ${VERSION}
  fi;

  # Deploy on GitHub
  git push origin github --tags

  # Create and deploy all docker images.
  wex wexample::images/rebuild -d -lsc -q
}
