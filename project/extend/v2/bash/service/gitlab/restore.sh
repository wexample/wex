#!/usr/bin/env bash

gitlabRestore() {
  # docs say we should run reconfigure at least once.
  wex app/exec -c="gitlab-ctl reconfigure"
  # lets check everything is working after first up.
  wex app/exec -c="gitlab-rake gitlab:check SANITIZE=true"
  # Stop services.
  wex app/exec -c="gitlab-ctl stop unicorn && gitlab-ctl stop sidekiq"
  # Prevent access limitations.
  wex app/exec -c="chmod -R 775 /var/opt/gitlab/backups"
  wex app/exec -c='gitlab-rake gitlab:backup:restore RAILS_ENV=production --trace'
  wex app/exec -c="gitlab-ctl start"
  # now lets check again.
  wex app/exec -c="gitlab-rake gitlab:check SANITIZE=true"
}