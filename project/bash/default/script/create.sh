#!/usr/bin/env bash

scriptCreateArgs() {
  _DESCRIPTION="Create a new script in current user folder"
  _ARGUMENTS=(
    'name n "Full name of the script, i.e. some/thing " true'
  )
}

scriptCreate() {
  local PATTERN='^[a-zA-Z0-9]+\/[a-zA-Z0-9]+$'

  if [[ ! "${NAME}" =~ ${PATTERN} ]]; then
    _wexError "Script name can contains only alphanumerical and should contain one slash, pattern : ${PATTERN}"
    return
  fi

  local FILE
  local DIR
  local PARTS
  local METHOD

  FILE="${WEX_RUNNER_PATH_WEX}bash/${NAME}.sh"
  DIR=$(dirname "${FILE}")

  mkdir -p "${DIR}"

  PARTS=($(wex string/split -t=${NAME} -s=/))

  METHOD="${PARTS[0]}$(_wexUpperCaseFirstLetter "${PARTS[1]}")"

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
  # Your arg "name" are accessible calling ${NAME}.
}

EOF

  echo "${FILE}"
}
