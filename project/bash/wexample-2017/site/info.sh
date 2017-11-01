#!/usr/bin/env bash

siteInfo() {
  echo -e "  Machine name : \t "${PWD##*/}
  echo -e "  Framework : \t\t "$(wex framework/detect -d="project")
}
