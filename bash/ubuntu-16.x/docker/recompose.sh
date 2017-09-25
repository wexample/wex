#!/usr/bin/env bash

dockerRecompose() {
  wex docker/stopAll
  wex docker/compose "$@"
}
