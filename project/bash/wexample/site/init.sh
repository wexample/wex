#!/usr/bin/env bash

siteInitArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root site directory" false'
 )
}

siteInit() {
  # Copy base files.
  cp -n -R ${WEX_DIR_ROOT}samples/site/. .

  git init

  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  cd ${DIR}

  echo "SITE_ENV=local" > .env

  # Name is current dir name.
  NAME="$(basename $( realpath "${DIR}" ))"

 if [ ! -f "wex.json" ]; then
  cat <<EOF > wex.json
{
  "name" : "${NAME}",
  "author" : "$(whoami)",
  "created" : "$(date -u)"
}
EOF
  fi;

  # No project dir
  if [ ! -d project ]; then
    # Create default dir
    mkdir project
    echo -e ${NAME}"\n===" > project/README.txt
    git add project/README.txt
  fi;

  # Already exist
  if [ -f ".gitignore" ]; then
    # Append ignore content
    cat .gitignore.demo >> .gitignore
    rm -f .gitignore.demo
  else
    mv .gitignore.demo .gitignore
  fi;

  git add .

  git commit -m"First wex commit"

  echo ""
  wex site/info
}
