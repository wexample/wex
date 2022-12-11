#!/usr/bin/env bash

ymlParseFileArgs() {
  _ARGUMENTS=(
    'file_yml f "File" true'
  )
}

# Convert file to bash variables
# replacing indents by underscores.
ymlParseFile() {
   local prefix=${2}
   local s='[[:space:]]\{0,\}' w='[a-zA-Z0-9_]\{0,\}' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\(${s}\):|\1|" \
        -e "s|^\(${s}\)\(${w}\)${s}:${s}[\"']\(.\{0,\}\)[\"']${s}\$|\1${fs}\2${fs}\3|p" \
        -e "s|^\(${s}\)\(${w}\)${s}:${s}\(.\{0,\}\)${s}\$|\1${fs}\2${fs}\3|p" "${FILE_YML}" |
   awk -F"${fs}" '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'${prefix}'",vn, $2, $3);
      }
   }'
}
