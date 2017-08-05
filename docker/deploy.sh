#!/usr/bin/env bash

docker build -t wexample/wexubuntu16:latest wexubuntu16 --no-cache
docker build -t wexample/wexwebserver:latest wexwebserver --no-cache
docker build -t wexample/wexphp7:latest wexphp7 --no-cache

docker login

docker push wexample/wexubuntu:latest
docker push wexample/wexwebserver:latest
docker push wexample/wexphp7:latest
