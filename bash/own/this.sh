
ownThisArgs() {
  _DESCRIPTION="Changing ownership of current directory to default user"
  _ARGUMENTS=(
    'file f "File" false .'
  )
}

ownThis() {
  sudo chown -R "${WEX_RUNNER_USERNAME}:${WEX_RUNNER_USERNAME}" "${FILE}"
}