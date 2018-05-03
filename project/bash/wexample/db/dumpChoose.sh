#!/usr/bin/env bash

dbDumpChoose() {
  FILES=($(ls mysql/dumps))

  while true; do
    read -p "Choose a db dump (1 to ${#FILES[@]}) : " ANSWER
    ((ANSWER--))
    if [ ${FILES[${ANSWER}]} ];then
      DUMP=${FILES[${ANSWER}]}
      break;
    fi;
  done

  echo ${DUMP}
}
