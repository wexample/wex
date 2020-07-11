#!/usr/bin/env bash

appEnv() {
  wex bash/readVar -f=.env -k=SITE_ENV
}