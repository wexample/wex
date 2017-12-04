sudoerAddArgs() {
  _ARGUMENTS=(
    [0]='user_name u "User name" true'
  )
}

sudoerAdd() {
  adduser ${USER_NAME}
  usermod -aG sudo ${USER_NAME}
}
