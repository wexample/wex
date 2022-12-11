#!/usr/bin/env bash

miscHelloWorldArgumentArgs() {
 _ARGUMENTS=(
   [0]='name n "Name of user" true'
   [1]='group g "Name of group" true'
   [2]='bye b "Bye" false'
 )
}

miscHelloWorldArgument() {
  echo "Hello World! - You are ${NAME} from ${GROUP}"
  if [ ! -z ${BYE+x} ]; then
    echo "Bye!"
  fi
}
