#!/usr/bin/env bash

gitlabRestore() {
  # docs say we should run reconfigure at least once.
  wex site/exec -c="gitlab-ctl reconfigure"
  # lets check everything is working after first up.
  wex site/exec -c="gitlab-rake gitlab:check SANITIZE=true"
  # Stop services.
  wex site/exec -c="gitlab-ctl stop unicorn && gitlab-ctl stop sidekiq"
  # Prevent access limitations.
  wex site/exec -c="chmod -R 775 /var/opt/gitlab/backups"
  wex site/exec -c='gitlab-rake gitlab:backup:restore RAILS_ENV=production --trace'
  wex site/exec -c="gitlab-ctl start"
  # now lets check again.
  wex site/exec -c="gitlab-rake gitlab:check SANITIZE=true"
}