
fileLineExists() {
  FILE=${1}
  LINE=${2}

  # Search for matching line
  results=$(grep -F "${LINE}" ${FILE})

  # Search if line exists
  grep -F "${LINE}" ${FILE} | while read -r result ; do
    if [ "${result}" == "${LINE}" ]; then
      echo true
      return
    fi
  done

}
