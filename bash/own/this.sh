
ownThisArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Changing ownership of current directory to default user"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" false .'
  )
}

ownThis() {
  sudo chown -R "${WEX_RUNNER_USERNAME}:${WEX_RUNNER_USERNAME}" "${FILE}"
}