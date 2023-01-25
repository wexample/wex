
ownThisArgs() {
  _DESCRIPTION="Changing ownership of current directory to default user"
  _AS_SUDO=false
  _AS_SUDO_RUN=true
  _ARGUMENTS=(
    'file f "File" false .'
  )
}

ownThis() {
  sudo chown -R "${WEX_RUNNER_USERNAME}:${WEX_RUNNER_USERNAME}" "${FILE}"
}