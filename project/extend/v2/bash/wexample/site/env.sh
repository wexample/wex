#!/usr/bin/env bash

siteEnv() {
  wex bash/readVar -f=.env -k=SITE_ENV
}