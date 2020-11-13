#!/usr/bin/env bash

imagesFlush() {
  # Remove all images from wexample
  docker rmi $(docker images wexample/* -q)
}
