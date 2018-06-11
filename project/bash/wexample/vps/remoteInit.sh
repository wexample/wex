#!/usr/bin/env bash

vpsRemoteInitArgs() {
 _ARGUMENTS=(
   [0]='host h "Server host address" true'
   [1]='user u "Root username for first access" true'
   [2]='password pw "SSH Password" false'
   [3]='port p "SSH Port" false'
 )
}

vpsRemoteInit() {
  ssh -q ${USER}@${HOST} "ls -la"
}