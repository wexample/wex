#!/usr/bin/env bash

sitePublish() {
  local RENDER_BAR='wex render/progressBar -w=30 '

  # Status -------- #
  ${RENDER_BAR} -p=0 -s="Loading env"

  . .env

  if [ ${SITE_ENV} != local ];then
    echo "You don't want to do that."
    exit
  fi

  # Check git version
  local GIT_VERSION=$(git version | sed 's/^git version \(.*\)$/\1/g')
  if [ $(wex text/versionCompare -a=${GIT_VERSION} -b=2.10) == '<' ];then
    echo "Your GIT version should be equal or higher to 2.10 and is actually at "${GIT_VERSION}"."
    exit;
  fi

  # Has internet.
  if [ $(wex network/hasInternet) == false ];then
    echo "Internet connexion is required"
    exit;
  fi

  # Status -------- #
  ${RENDER_BAR} -p=10 -s="Init connexion info"

  # Save connection info.
  wex wexample::remote/init

  # Use same key for Gitlab && production
  local REPO_SSH_PRIVATE_KEY=$(wex ssh/keySelect -s -n="REPO_SSH_PRIVATE_KEY" -d="SSH Private key for Gitlab")

  # Status -------- #
  ${RENDER_BAR} -p=20 -s="Loading configuration"
  # Load generated configuration.
  wexampleSiteInitLocalVariables
  . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}

  # Load base configuration.
  wex config/load

  # Use local private key as deployment key
  git config core.sshCommand "ssh -i "${REPO_SSH_PRIVATE_KEY}

  # Status -------- #
  ${RENDER_BAR} -p=30 -s="Creating Gitlab repo"

  local GIT_ORIGIN=$(git config --get remote.origin.url)

  # We need to create repository.
  if [ $(wex repo/exists) == false ];then
    # Old origin saved locally
    if [ "${GIT_ORIGIN}" != '' ];then
      # Remove corrupted origin.
      git remote rm origin
      GIT_ORIGIN=''
    fi
    # Create new repo.
    wex repo/create
  fi

  # Status -------- #
  ${RENDER_BAR} -p=40 -s="Push on Gitlab"

  # Get origin.
  local NEW_ORIGIN=$(wex repo/info -k=ssh_url_to_repo -cc)

  if [ "${GIT_ORIGIN}" != "${NEW_ORIGIN}" ];then
      # Add origin
      git remote add origin ${GIT_ORIGIN}
  fi

  NEW_ORIGIN=${GIT_ORIGIN}

  # Status -------- #
  ${RENDER_BAR} -p=50 -s="Push on Gitlab"

  git add .
  git commit -m "site/publish"
  git push -q -u origin master

  # Status -------- #
  ${RENDER_BAR} -p=60 -s="Configure remote Git repository"

  # Test connexion between gitlab <---> prod
  local GITLAB_PROD_EXISTS=$(wex remote/exec -e=prod -d="/" -s="wex git/remoteExists -r=${GIT_ORIGIN}")

  # Remove special chars ma be due to remote data transfer.
  GITLAB_PROD_EXISTS=$(echo "${GITLAB_PROD_EXISTS}" | tr -dc '[:alnum:]\n')

  # Usable to connect Gitlab / Production
  if [ "${GITLAB_PROD_EXISTS}" == false ];then
    wex text/color -c=red -t='Production server is unable to connect to Gitlab'

    local GITLAB_DOMAIN=$(echo ${GIT_ORIGIN} | sed 's/git@\(.*\):.*$/\1/g')
    local REPO_NAMESPACE=$(wex repo/namespace)

    echo -e 'You may need to enable deployment key on \nhttp://'${GITLAB_DOMAIN}'/'${REPO_NAMESPACE}'/'${SITE_NAME}'/settings/repository.\n'
    exit;
  fi

  # Status -------- #
  ${RENDER_BAR} -p=70 -s="Clone in production"

  local DIR_EXISTS=$(wex remote/exec -e=prod -d="/var/www" -s="[[ -d videos ]] && echo true || echo false")
  if [ ${DIR_EXISTS} == true ];then
    wex text/color -c=red -t='Directory exists in production.'
    exit
  fi

  # Clone remote repository.
  wex remote/exec -e=prod -d="/var/www" -s="git clone "${GIT_ORIGIN}" "${SITE_NAME}

  # Copy local files to production.
  wex files/push -e=prod

  # TODO services exec (mysql)

  # Status -------- #
  ${RENDER_BAR} -p=80 -s="Enable auto deployment"

  # Save production server host for deployment.
  wex json/addValue -f=wex.json -k="prod.ipv4" -v=${SSH_HOST}
  git add wex.json
  git commit -m "Auto publication"
  git push origin master

  # Status -------- #
  ${RENDER_BAR} -p=80 -s="Enable auto deployment"

  # Create production env file
  wex remote/exec -e=prod -s="echo SITE_ENV=prod > .env"
  # Start site
  wex remote/exec -e=prod -s="wex site/start"

  # Status -------- #
  ${RENDER_BAR} -p=100 -s="Done"

}
