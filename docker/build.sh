#!/usr/bin/env bash

docker build -t wexample/wexubuntu:latest wexubuntu16
docker build -t wexample/wexwebserver:latest wexwebserver
docker build -t wexample/wexphp7:latest wexphp7
