#!/usr/bin/env bash

docker build -t wexample/wexubuntu16:latest wexubuntu16
docker build -t wexample/wexwebserver:latest wexwebserver
docker build -t wexample/wexphp7:latest wexphp7

docker login

docker push wexample/wexubuntu:latest
docker push wexample/wexwebserver:latest
docker push wexample/wexphp7:latest
