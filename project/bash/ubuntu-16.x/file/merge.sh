#!/usr/bin/env bash

fileMergeArgs() {
  _ARGUMENTS=(
    [0]='source_file s "Source file to merge and delete." true'
    [1]='dest_file d "Dest file to append content" true'
    [2]='keep_source k "Do note delete source" false'
  )
}

fileMerge() {
  # File exists.
  if [[ -f ${SOURCE_FILE} ]];then
    # Append ignore content
    cat ${SOURCE_FILE} >> ${DEST_FILE}
    if [[ ${KEEP_SOURCE} == true ]];then
      rm -f ${SOURCE_FILE}
    fi;
  fi;
}
