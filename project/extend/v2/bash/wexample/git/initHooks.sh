#!/usr/bin/env bash

# We just append command on git hooks
# We don't check if hooks already exists.
gitInitHooks() {
  local PATH_GIT_HOOKS=.git/hooks/
  local PATH_PROJECT_GIT_HOOKS=./script/git_hooks/
  local GIT_HOOKS=$(ls ${PATH_PROJECT_GIT_HOOKS})

  # Remove existing broken symlinks
  find ${PATH_GIT_HOOKS} -maxdepth 1 -follow -type l -delete

  for GIT_HOOK in ${GIT_HOOKS[@]}
  do
    # Rebuild symlink.
    ln -sf ../../${PATH_PROJECT_GIT_HOOKS}${GIT_HOOK} ${PATH_GIT_HOOKS}${GIT_HOOK}
  done
}
