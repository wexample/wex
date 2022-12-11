#!/usr/bin/env bash

laravel5AppBuild() {
    # Same as web
  . ${WEX_DIR_SERVICES}node/hooks/appBuild.sh

  nodeAppBuild
}