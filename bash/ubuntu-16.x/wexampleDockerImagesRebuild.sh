#!/usr/bin/env bash

wexampleDockerImagesRebuild() {
  docker build -t wexample/wexubuntu16:latest docker/wexubuntu16
  docker build -t wexample/wexwebserver:latest docker/wexwebserver
  docker build -t wexample/wexphp7:latest docker/wexphp7
}
