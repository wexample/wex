#!/usr/bin/env bash

# Generate a version.
VERSION=$(wex version/generate -v=2)

# Add tag if not exists.
if [ $(wex git/tagExists -t=${VERSION}) == false ];then
  # Create a tag.
  git tag ${VERSION}
fi;
