#!/usr/bin/env bash

siteCreate() {
  # Init if not a wex site.
  if [ ! -f "wex.json" ]; then
    wex wexample::site/init
  fi

  wex gitlab/namespaceId -u="http://gitlab.wexample.com/api/v4/"

  # TODO Create
  #wex wexample::gitlab/post -d="path=testapi&namespace_id=wexample" -q="projects"
  #wex wexample::gitlab/post -d="path=testapi&namespace_id=wexample" -q="projects"

  # TODO Get
  # wex wexample::gitlab/get -q="projects"

  # TODO Delete
  #wex wexample::gitlab/delete -q="projects/weeger%2Ftestapi"

  #local SITE_NAME=$(wex site/config -k=name)



  #wget ${WEX_GITLAB_URL}/projects/wexample

  #echo ${GITLAB_TOKEN}
  #git init

  #git add origin mas

}
