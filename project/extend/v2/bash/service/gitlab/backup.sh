#!/usr/bin/env bash

gitlabBackup() {
  wex app/exec -c="gitlab-rake gitlab:backup RAILS_ENV=production"
}