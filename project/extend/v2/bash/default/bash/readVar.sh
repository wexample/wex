#!/usr/bin/env bash

bashReadVarArgs() {
  _ARGUMENTS=(
    [0]='file f "File to read" true'
    [1]='key k "Key to find in env config" true'
    [2]='ask a "Prompt user if not defined" false'
    [3]='label l "Description of the variable" false'
    [4]='write w "Write new variable in file" false'
    [5]='default d "Default value if not defined" false'
  )
}

bashReadVar() {
  # Empty if variable is not
  unset ${KEY}
  # Load env file
  . ${FILE}

  # Get the key value
  eval VALUE='$'${KEY}

  local VALUE_FOUND=true

  # Value does not exists.
  if [ "${VALUE}" == "" ]; then
    VALUE_FOUND=false
    # Ask user
    if [ "${ASK}" == true ];then
      # Description found
      if [ ! -z ${LABEL+x} ];then
        DESC=${LABEL}
      else
        DESC=${KEY}
      fi

      # Default value set
      if [ ! -z ${DEFAULT+x} ];then
        # Display it in message
        DESC+=" [${DEFAULT}]"
      fi

      read -p "${DESC} : " VALUE
    fi
  fi

  # Still no value even user may be asked
  if [ "${VALUE}" == "" ] && [ ! -z ${DEFAULT+x} ]; then
    VALUE_FOUND=false
    VALUE=${DEFAULT}
  fi

  if [ "${WRITE}" == true ] && [ "${VALUE_FOUND}" == false ];then
    CONTENT=""
    # Set description as comment
    if [ ! -z ${LABEL+x} ];then
      CONTENT+="\n# ${LABEL}"
    fi
    # Use quote as it is a bash file.
    CONTENT+="\n${KEY}=\"${VALUE}\""
    # Append.
    echo -e ${CONTENT} >> ${FILE}
  fi

  echo ${VALUE}
}
