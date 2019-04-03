#!/usr/bin/env bash

sshConvertToPPKArgs() {
  _DESCRIPTION="Convert a SSH key to the PPK format."
  _ARGUMENTS=(
    [0]='type t '"'"'The kind of key to convert : "private" or "public"'"'"' true'
    [1]='source s "The source file path." true'
    [2]='destination d "The destination file path. If not specified, the source file will be overwritten." false'
  )
}

sshConvertToPPK() {
  # if the puttygen command exists then
  if hash puttygen 2>/dev/null; then

    # if there is no destination parameter, then the file is overwritten
    if [[ -z "${DESTINATION}" ]]; then
      local DESTINATION=${SOURCE}
    fi

    if [[ "${TYPE}" == "private" ]]; then
      local result=$(puttygen ${SOURCE} -O private -o ${DESTINATION} 2>&1)
    else
      local result=$(puttygen ${SOURCE} -p -o ${DESTINATION} 2>&1)
    fi

    # if puttygen has successfully made his work...
    if [[ "${RESULT}" == "" ]]; then
      wex text/color -c=green -t="Your ${TYPE} key has been successfully converted to PPK format.";
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
