#!/usr/bin/env bash

systemCleanup() {
  apt-get clean
  apt-get autoremove
}