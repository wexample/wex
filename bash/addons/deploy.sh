#!/usr/bin/env bash

addonsDeploy() {
  chown -R gitlab-runner:gitlab-runner "${WEX_DIR_ROOT}"
  local OWNER="sudo -u gitlab-runner -H"

  for ADDON in "${WEX_ADDONS[@]}"; do
    if [ -d "${WEX_DIR_ADDONS}${ADDON}" ]; then
      _wexLog "Changing origin for ${ADDON}..."
      git -C "${WEX_DIR_ROOT}/addons/$ADDON" config remote.origin.url ssh://git@gitlab.wexample.com:4567/wexample/wex-addon-$ADDON.git;

      _wexLog "Pushing ${ADDON}..."

      cd "${WEX_DIR_ADDONS}${ADDON}"
      ${OWNER} git pull --no-rebase
      ${OWNER} git checkout -b develop
      ${OWNER} git checkout master
      ${OWNER} git merge --no-ff develop
      ${OWNER} git push origin master
    fi
  done

  chown -R root:root "${WEX_DIR_ROOT}"
}
