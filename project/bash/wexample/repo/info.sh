#!/usr/bin/env bash
repoInfoArgs() {
  _ARGUMENTS=(
    [0]='clear_cache cc "Clear cache" false'
    [1]='key k "Clear cache" false'
  )
}

repoInfo() {
  local CACHE=${WEX_WEXAMPLE_SITE_DIR_TMP}"repoInfo.json"
  if [ ! -f ${CACHE} ] || [ "${CLEAR_CACHE}" == true ];then
    local REPO_NAME=$(wex repo/name);
    local INFO=$(wex wexample::gitlab/get -p="projects/${REPO_NAME}")
    echo -e ${INFO} > ${CACHE}
  fi

  if [ "${KEY}" != "" ];then
    cat ${CACHE} | sed -E 's/^.\{0,\}\"'${KEY}'\"\:\"([^\"]\{0,\}).\{0,\}$/\1/'
  else
    cat ${CACHE}
  fi
}
