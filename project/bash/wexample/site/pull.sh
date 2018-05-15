#!/usr/bin/env bash

sitePull() {
  #!/usr/bin/env bash

  # Used in production to retrieve changes when tests are passed.

  # This file should be executed from the site root.

  # We are in the host server.
  if [ $(wex docker/isEnv) == false ]; then
    # Stop during pull
    wex site/stop

    # Update GIT
    wex git/pullTree

    # Run itself into container, see below.
    wex site/exec -c="wex wexample::site/pull"

    # Restart.
    wex site/start
  else

    SITE_PATH_ROOT=/var/www/html/

    # Go to current (container) folder.
    cd ${SITE_PATH_ROOT}

    # Manage permissions.
    chown -R www-data:www-data ./

    # Per framework pull behavior.
    # Detect used frameworks
    FRAMEWORKS=($(wex framework/list -d=./project/))

    for FRAMEWORK in ${FRAMEWORKS[@]}
    do
      FRAMEWORK=framework$(wexUpperCaseFirstLetter ${FRAMEWORK})
      # Pull script exists
      if [ -f ${WEX_DIR_BASH}"wexample/"${FRAMEWORK}"/pull.sh" ];then
        wex wexample::${FRAMEWORK}/pull
      fi
    done;

    wex ci/exec -c=pull
  fi;
}
