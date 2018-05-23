#!/usr/bin/env bash

dockerIsToolBox() {
  if [ $(docker-machine ls -q | grep box) ];then
    echo true
  else
    echo false
  fi
}
