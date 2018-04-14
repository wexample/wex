#!/usr/bin/env bash

siteCreate() {
  # Init if not a wex site.
  if [ ! -f "wex.json" ]; then
    wex wexample::site/init
  fi

  wex gitlab/namespaceId -u="http://gitlab.wexample.com/api/v4/"

  # TODO Get
  # wex wexample::gitlab/get -p="projects"

  # TODO Delete
  #wex wexample::gitlab/delete -q="projects/weeger%2Ftestapi"

  #local SITE_NAME=$(wex site/config -k=name)



  #wget ${WEX_GITLAB_URL}/projects/wexample

  #echo ${GITLAB_TOKEN}
  #git init

  #git add origin mas

}
