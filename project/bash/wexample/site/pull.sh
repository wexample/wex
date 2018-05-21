#!/usr/bin/env bash

sitePull() {
  #!/usr/bin/env bash

  # Used in production to retrieve changes when tests are passed.

  # Update GIT and submodules.
  wex git/pullTree

  wex service/exec -c=sitePull

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
}
