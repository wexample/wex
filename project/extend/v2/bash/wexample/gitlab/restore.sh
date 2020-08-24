#!/usr/bin/env bash

gitlabRestore() {
  wex app/exec -c="gitlab-rake gitlab:backup:restore RAILS_ENV=production"
}