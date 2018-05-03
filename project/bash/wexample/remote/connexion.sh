#!/usr/bin/env bash

remoteConnexionArgs() {
  _ARGUMENTS=(
    [0]='ssh_user_custom u "SSH User" false'
    [1]='ssh_private_key_custom k "SSH Private key" false'
    [2]='ssh_host_custom h "Host to connect to" false'
    [3]='ssh_port_custom p "SSH Port" false'
    [4]='environment e "Environment to connect to" true'
  )
}

remoteConnexion() {
  local ENV=$(wex text/uppercase -t="${ENVIRONMENT}")

  # Try with local variables (local environment).
  if [ -f ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE} ];then
    wexampleSiteInitLocalVariables
    . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}
  # Try with versioned variables (pipeline)
  else
    . .wex
  fi

  if [ "${SSH_USER_CUSTOM}" != "" ];then
    local SSH_USER=${SSH_USER_CUSTOM}
  else
    # Get value
    local SSH_USER=$(eval 'echo ${'${ENV}'_SSH_USER}')
  fi

  if [ "${SSH_HOST_CUSTOM}" != "" ];then
    local SSH_HOST=${SSH_HOST_CUSTOM}
  else
    # Get value
    local SSH_HOST=$(eval 'echo ${'${ENV}'_SSH_HOST}')
  fi

  if [ "${SSH_PORT_CUSTOM}" != "" ];then
    local SSH_PORT=${SSH_PORT_CUSTOM}
  else
    # Get value
    local SSH_PORT=$(eval 'echo ${'${ENV}'_SSH_PORT}')
  fi

  if [ "${SSH_PRIVATE_KEY_CUSTOM}" != "" ];then
    local SSH_PRIVATE_KEY=${SSH_PRIVATE_KEY_CUSTOM}
  else
    # Get value
    local SSH_PRIVATE_KEY=$(eval 'echo ${'${ENV}'_SSH_PRIVATE_KEY}')
  fi

  # Default port
  if [ "${SSH_PORT}" == "" ];then
    SSH_PORT=22
  fi

  echo "-i${SSH_PRIVATE_KEY} -t -p${SSH_PORT} ${SSH_USER}@${SSH_HOST}"
}
