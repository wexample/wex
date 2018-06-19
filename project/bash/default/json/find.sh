#!/usr/bin/env bash

jsonFindArgs() {
 _ARGUMENTS=(
   [0]='json j "Content to search into" true'
   [1]='key k "Search key" true'
   [2]='num n "Return only this result" false'
 )
}

# Print an array of found values
jsonFind() {
  echo ${JSON} | awk -F"[,:}]" '{for(i=1;i<=NF;i++){if($i~/'${KEY}'\042/){print $(i+1)}}}' | tr -d '"' | sed -n ${NUM}p
}