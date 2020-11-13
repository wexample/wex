#!/usr/bin/env bash

# Based on config files, commit and push automatically some folders.
gitAutoPush() {
  . .wex

  local SITE_ENV=$(wex site/env)
  local SITE_ENV_MAJ=${SITE_ENV^^}
  local GIT_AUTO_PUSH=($(eval 'echo ${'${SITE_ENV_MAJ}'_GIT_AUTO_PUSH[@]}'))

  if [ ! -z ${GIT_AUTO_PUSH} ];then
    # Load used ports in all sites.
    for PATH_VERSIONED in ${GIT_AUTO_PUSH[@]}
    do
      if [[ "$(wex git/hasChanges -p="${PATH_VERSIONED}")" == true ]]; then
        git add ${PATH_VERSIONED}
        git commit -m "git/autoPush "${PATH_VERSIONED}
        git push
      fi
    done
  fi
}