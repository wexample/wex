
fileLineExists() {
  FILE=${1}
  LINE=${2}

  # Protect arguments, escape \ / $
  LINE=$(sed 's/\\/\\\\/g' <<< "${LINE}")
  LINE=$(sed 's/\//\\\//g' <<< "${LINE}")
  LINE=$(sed 's/\$/\\$/g' <<< "${LINE}")

  results=$(sed -n "s/^\(${LINE}\)$/\1/p" ${FILE})

  if [ "${results}" != "" ]; then
    echo true
    return
  fi

  echo false
}
