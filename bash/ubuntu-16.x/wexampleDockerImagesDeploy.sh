#!/usr/bin/env bash

wexampleDockerImagesDeploy() {
  docker login

  docker push wexample/wexubuntu16:latest
  docker push wexample/wexwebserver:latest
  docker push wexample/wexphp7:latest
}
