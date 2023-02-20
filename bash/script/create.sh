#!/usr/bin/env bash

scriptCreateArgs() {
  _DESCRIPTION="Create a new script in current user folder"
  _ARGUMENTS=(
    'Script s "Full name of the script, i.e. some/thing " true'
  )
}

scriptCreate() {
  . "${WEX_DIR_ROOT}includes/script.sh"

  if [[ ! "${SCRIPT}" =~ ^${WEX_SCRIPT_NAME_REGEX}+$ ]]; then
    _wexError "Script name can contains only alphanumerical and should contain one slash, pattern : ${PATTERN}"
    return
  fi

  local FILE
  local DIR
  local METHOD

  FILE=$(_wexLocalScriptPath "${SCRIPT}")
  DIR=$(dirname "${FILE}")
  METHOD="$(_wexMethodName "${SCRIPT}")"

  mkdir -p "${DIR}"

  cat <<EOF > "${FILE}"
#!/usr/bin/env bash

${METHOD}Args() {
  _DESCRIPTION="Custom script"
  _ARGUMENTS=(
    # [arg_name] [arg_name_short] [description] [required] [default_value]
    # 'name n "Name" true "defaultName"'
  )
}

${METHOD}() {
  # Your script body.
  # Your arg "name" are accessible calling ${SCRIPT}.
  echo "Do something."
}

EOF

  # Create test
  FILE="$(realpath "${WEX_RUNNER_PATH_BASH}../")/tests/bash/${SCRIPT}.sh"
  DIR=$(dirname "${FILE}")

  mkdir -p "${DIR}"

  cat <<EOF > "${FILE}"
#!/usr/bin/env bash

${METHOD}Test() {
  # Your test body. i.e :
  #   _wexTestAssertEqual "${A}" "A"
  #   _wexTestAssertNotEmpty "${A}"
  echo "Create a test"
}

EOF

  echo "${FILE}"

  wex-exec core/register
}
