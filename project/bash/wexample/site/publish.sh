#!/usr/bin/env bash

sitePublishArgs() {
  _ARGUMENTS=(
    [0]='recreate r "Restart publishing configuration" false'
  )
}

sitePublish() {
  local RENDER_BAR='wex render/progressBar -w=30 '

  # Status
  ${RENDER_BAR} -p=0 -s="Loading env" -nl

  . .env
  . .wex

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

  # Status
  ${RENDER_BAR} -p=10 -s="Init production connexion info" -nl

  # Save connection info.
  wex wexample::remote/init -r=${RECREATE}

  # Clear local variables.
  if [ "${RECREATE}" == true ];then
    wex wexample::var/localClear -n=GITLAB_URL_DEFAULT
  fi

  # Use same key for Gitlab && production
  local PROD_SSH_PRIVATE_KEY=$(wex var/localGet -r -s -n="PROD_SSH_PRIVATE_KEY" -d="")
  local REPO_SSH_PRIVATE_KEY=${PROD_SSH_PRIVATE_KEY}
  local PROD_SSH_HOST=$(wex var/localGet -r -n="PROD_SSH_HOST")
  local GITLAB_URL=$(wex wexample::var/localGet -n=GITLAB_URL_DEFAULT -d="${WEX_GITLAB_URL}")
  local GIT_ORIGIN=$(git config --get remote.origin.url)

  # Load generated configuration.
  wexampleSiteInitLocalVariables
  . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}

  # Load base configuration.
  wex config/load

  # Create repo
  ${RENDER_BAR} -p=20 -s="Create repo" -nl

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

   # Get origin.
  local NEW_ORIGIN=$(wex repo/info -k=ssh_url_to_repo -cc)

  if [ "${GIT_ORIGIN}" != "${NEW_ORIGIN}" ];then
      # Add origin
      git remote add origin ${NEW_ORIGIN}
  fi

  GIT_ORIGIN=${NEW_ORIGIN}

  # Test connexion to repo
  if [ $(wex git/remoteExists -r=${GIT_ORIGIN}) == false ];then
    echo ''
    echo -e 'Git origin '${GIT_ORIGIN}' is not reachable'
    echo -e 'You may need to add your public SSH key associated with '${PROD_SSH_PRIVATE_KEY}' at http://'${GITLAB_URL}'/profile/keys'
    exit;
  fi

  # Use local private key as deployment key
  git config core.sshCommand "ssh -i "${REPO_SSH_PRIVATE_KEY}

  # Status
  ${RENDER_BAR} -p=30 -s="Allow production server key"

  # Get production rsa key
  local PROD_ID_RSA_PUB=$(wex remote/exec -q -e=prod -d="/" -s="cat /root/.ssh/id_rsa.wex.gitlab.pub")
  # Remove \r carriage
  PROD_ID_RSA_PUB=$(echo "${PROD_ID_RSA_PUB}"|tr -d '\r')
  # Find registered id for production key if exists.
  local PROD_KEY_ID=$(wex gitlab/keyId -k="${PROD_ID_RSA_PUB}")

  local REPO_NAME=$(wex repo/name);
  wex wexample::gitlab/post -p="projects/${REPO_NAME}/deploy_keys/"${PROD_KEY_ID}"/enable" &> /dev/null

  # Status
  ${RENDER_BAR} -p=32 -s="Init repo to production connexion"

  # Test connexion between gitlab <---> prod
  local GITLAB_PROD_EXISTS=$(wex remote/exec -q -e=prod -d="/" -s="wex git/remoteExists -r=${GIT_ORIGIN}")
  # Remove \r carriage
  GITLAB_PROD_EXISTS=$(echo "${GITLAB_PROD_EXISTS}" |tr -d '\r')

  # Unable to connect Gitlab / Production
  if [ "${GITLAB_PROD_EXISTS}" == false ];then
    echo ''
    wex text/color -c=red -t='Production server is unable to connect to Gitlab'

    local GITLAB_DOMAIN=$(echo ${GIT_ORIGIN} | sed 's/git@\(.*\):.*$/\1/g')
    local REPO_NAMESPACE=$(wex repo/namespace)

    echo -e 'You may need to enable deployment key on \nhttp://'${GITLAB_URL}'/'${REPO_NAMESPACE}'/'${SITE_NAME}'/settings/repository.\n'
    exit;
  fi

  # Status
  ${RENDER_BAR} -p=35 -s="Clone repo on production"

  local DIR_EXISTS=$(wex remote/exec -q -e=prod -d="/var/www" -s="[[ -d ${SITE_NAME} ]] && echo true || echo false")
  # Remove special chars may be due to remote data transfer.
  DIR_EXISTS=$(echo "${DIR_EXISTS}" | tr -dc '[:alnum:]\n')
  if [ ${DIR_EXISTS} == true ];then
    wex text/color -c=red -t='Directory '${SITE_NAME}' exists in production.'
    exit
  fi

  # Clone on remote repository.
  wex remote/exec -q -e=prod -d="/var/www" -s="git clone "${GIT_ORIGIN}" "${SITE_NAME}
  # Create production env file
  wex remote/exec -q -e=prod -d="/var/www/${SITE_NAME}" -s="echo SITE_ENV=prod > .env"

  # Status
  ${RENDER_BAR} -p=40 -s="Push on Gitlab"

  # Save production server host for deployment.
  echo "PROD_SSH_HOST="${PROD_SSH_HOST} >> .wex
  echo "PROD_SSH_PORT="${PROD_SSH_PORT} >> .wex

  git add .
  git commit -m "site/publish"
  git push -q -u origin master

  echo -e "Waiting auto deployment...\r"
  while [ $(wex pipeline/ready) == false ];do
    echo -e ".\r"
    sleep 2
  done

  # Status
  ${RENDER_BAR} -p=50 -s="Copy files in production"

  # Copy local files to production.
  wex files/push -e=prod

  # Execute per service publication (database migration, etc...)
  wex service/exec -c=publish

  # Start site
  wex remote/exec -q -e=prod -s="wex site/start"

  # Status
  ${RENDER_BAR} -p=100 -s="Done" -nl

}
