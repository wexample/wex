#!/usr/bin/env bash

wexampleDockerImagesRebuild() {
  docker build -t wexample/wexubuntu16:latest wexubuntu16
  docker build -t wexample/wexwebserver:latest wexwebserver
  docker build -t wexample/wexphp7:latest wexphp7
}
