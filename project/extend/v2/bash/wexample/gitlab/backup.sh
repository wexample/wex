#!/usr/bin/env bash

gitlabBackup() {
  wex site/exec -c="gitlab-rake gitlab:backup:create"
}