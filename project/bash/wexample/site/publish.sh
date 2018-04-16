#!/usr/bin/env bash

sitePublish() {
   local RENDER_BAR='wex render/progressBar -w=30 '

   # Status
   ${RENDER_BAR} -p=0 -s="Loading env"

  . .env

  if [ ${SITE_ENV} != local ];then
    echo "You don't want to do that."
    exit
  fi

  # Status
  ${RENDER_BAR} -p=5 -s="Init connexion info"

  # Save connection info.
  wex wexample::remote/init

  # Status
  ${RENDER_BAR} -p=10 -s="Loading configuration"

  # Load generated configuration.
  . ./tmp/variablesLocalStorage

  # Load base configuration.
  wex site/configLoad

  # ---- Create Gitlab repo ---- #

  # Status
  ${RENDER_BAR} -p=20 -s="Creating Gitlab repo"

  # No git origin.
  if [ "${GIT_ORIGIN}" == '' ];then
     # Search if repo exists and have origin.
     local REPO_ORIGIN=$(wex repo/info -k=ssh_url_to_repo)

     if [ "${REPO_ORIGIN}" == '' ];then
       # Ask user.
       local CREATE=$(wex prompt/yn -q="No repository origin, do you want to create it ?")
       if [ ${CREATE} == true ];then
         # Create new repo.
         wex repo/create
         # Get origin.
         local REPO_ORIGIN=$(wex repo/info -k=ssh_url_to_repo)
       fi
     fi
     # Add origin
     git remote add origin ${REPO_ORIGIN}
  fi

  # Status
  ${RENDER_BAR} -p=50 -s="Push on Gitlab"

  git add .
  git commit -m "site/publish"
  git push origin master

  # Status
  ${RENDER_BAR} -p=60 -s="Configure remote Git repository"

  local GIT_ORIGIN=$(git config --get remote.origin.url)

  # Test connexion between gitlab <---> prod
  local GITLAB_PROD_TEST=$(wex ssh/exec -e=prod -s="git ls-remote "${GIT_ORIGIN}" -h --exit-code &> /dev/null; echo \$?")

  local GITLAB_DOMAIN=$(echo ${GIT_ORIGIN} | sed 's/git@\(.*\):.*$/\1/g')
  local REPO_NAMESPACE=$(wex repo/namespace)
  # Error code returned.
  if [ "${GITLAB_PROD_TEST}" == 128 ];then
    wex text/color -c=red -t='Production server is unable to connect to Gitlab'
    echo -e 'You may need to enable deployment key on \nhttp://'${GITLAB_DOMAIN}'/'${REPO_NAMESPACE}'/'${SITE_NAME}'/settings/repository.\n'
    exit;
  fi

  # Status
  ${RENDER_BAR} -p=70 -s="Clone in production"

  # Clone remote repository.
  wex ssh/exec -e=prod -d="/var/www" -s="git clone "${GIT_ORIGIN}" "${SITE_NAME}

  # Copy local files to production.
  wex files/push -e=prod

  # Status
  ${RENDER_BAR} -p=90 -s="Enable auto deployment"

  # Save production server host for deployment.
  wex json/addValue -f=wex.json -k="prod.ipv4" -v=${SSH_HOST}
  git add wex.json
  git commit -m "Auto publication"
  git push origin master

  # Status
  ${RENDER_BAR} -p=100 -s="Done"

}
