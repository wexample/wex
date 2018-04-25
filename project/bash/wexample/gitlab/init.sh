#!/usr/bin/env bash

gitlabInit() {
  if [ -f ./.gitlab-ci.yml ];then
    cat ${WEX_DIR_SAMPLES}gitlab/.gitlab-ci.yml.source >> ./.gitlab-ci.yml
  else
    cp ${WEX_DIR_SAMPLES}gitlab/.gitlab-ci.yml.source ./.gitlab-ci.yml
  fi
}
