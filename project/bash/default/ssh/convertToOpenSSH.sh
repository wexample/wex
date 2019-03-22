#!/usr/bin/env bash

sshConvertToOpenSSHArgs() {
  _DESCRIPTION="Convert a SSH key to the OpenSSH format."
  _ARGUMENTS=(
    [0]='type t '"'"'The kind of key to convert : "private" or "public"'"'"' true'
    [1]='source s "The source file path." true'
    [2]='destination d "The destination file path. If not specified, the source file will be overwritten." false'
  )
}

# TODO Understan the case where puttygen says "puttygen: cannot perform this action on a public-key-only input file" and try to resolve it via this script
# This message appears when i'm not in the ~/.ssh folder
sshConvertToOpenSSH() {
  # if the puttygen command exists then
  if hash puttygen 2>/dev/null; then
    # if there is no destination parameter, then the file is overwritten
    if [[ -z "${DESTINATION}" ]]; then
      local DESTINATION=${SOURCE}
    fi

    if [[ "${TYPE}" == "private" ]]; then
      local RESULT=$(puttygen ${SOURCE} -O private-openssh -o ${DESTINATION} 2>&1)
    else
      local RESULT=$(puttygen ${SOURCE} -L -o ${DESTINATION} 2>&1)
    fi

    if [[ "${RESULT}" == "" ]]; then
      wex text/color -c=green -t="Your ${TYPE} key has been successfully converted to OpenSSH format.";
    else
      echo $(wex text/color -c=red -t="[ERROR]") "${RESULT}";
    fi

  else
    echo -e 'You must install Putty tools to launch this command.\n'
    echo '- Ubuntu' $(wex text/color -c=lightblue -t='sudo apt-get install putty-tools')
    echo '- Debian-like' $(wex text/color -c=lightblue -t='apt-get install putty-tools')
    echo '- RPM based' $(wex text/color -c=lightblue -t='yum install putty')
    echo '- Gentoo' $(wex text/color -c=lightblue -t='emerge putty')
    echo '- Archlinux' $(wex text/color -c=lightblue -t='sudo pacman -S putty')
  fi
}