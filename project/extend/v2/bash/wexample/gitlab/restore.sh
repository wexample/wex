#!/usr/bin/env bash

gitlabRestore() {
  wex site/exec -c="gitlab-rake gitlab:backup:restore RAILS_ENV=production"
}