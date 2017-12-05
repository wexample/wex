#!/usr/bin/env bash

sitePull() {
  #!/usr/bin/env bash

  # Used in production to retrieve changes when tests are passed.

  # This file should be executed from the site root.

  # We are in the host server.
  if [ $(wex docker/isEnv) == false ]; then

    # Revert to old mod before pull.
    chmod 644 -R *

    # Update GIT
    wex git/pullTree

    # Run itself into container, see below.
    wex site/exec -c="wex wexample::site/pull"

  else

    SITE_PATH_ROOT=/var/www/html/

    # Go to current (container) folder.
    cd ${SITE_PATH_ROOT}

    # Manage permissions.
    chmod 755 -R *
    chown www-data:www-data -R *

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

    # Execute custom script for site.
    if [ -f ci/pull.sh ];then
      . ci/pull.sh
    fi
  fi;
}
