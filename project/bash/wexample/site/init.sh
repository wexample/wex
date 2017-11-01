#!/usr/bin/env bash

siteInitArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root site directory" false'
 )
}

siteInit() {
  git init

  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  cd ${DIR}

  # Name is current dir name.
  NAME="$(basename $( realpath "${DIR}" ))"

  cat <<EOF > wex.json
{
  "name" : "${NAME}",
  "author" : "$(whoami)",
  "created" : "$(date -u)"
}
EOF

  git add wex.json

  # No project dir
  if [ ! -d project ]; then
    # Create default dir
    mkdir project
    echo -e ${NAME}"\n===" > project/README.txt
    git add project/README.txt
  fi;

  git commit -m"First wex commit"

  echo ""
  wex site/info
}
