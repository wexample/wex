#!/usr/bin/env bash

mysqlDiagArgs() {
  _ARGUMENTS=(
    [0]='container c "Container" false'
    [1]='user_mysql u "DB User" false'
    [2]='password p "DB Password" false'
  )
}

mysqlDiagOk() {
  local GREEN='\033[1;32m'
  local NC='\033[0m'
  echo -e "${GREEN}OK${NC} "${1}
}

mysqlDiagKo() {
  local RED="\033[0;31m"
  local NC='\033[0m'
  echo -e "${RED}OK${NC} "${1}
}

mysqlDiag() {

  if [[ "${CONTAINER}" == "" ]];then
    wex config/load

    CONTAINER=${SITE_NAME_INTERNAL}_mysql
  fi

  local LOGS=$(docker logs ${CONTAINER} 2>&1)
  local ERRORS=$(echo -e "${LOGS}" | grep "\[ERROR\]")

  if [[ "${ERRORS}" != "" ]];then
    mysqlDiagKo "Errors logged"
    echo -e "${ERRORS}"
  else
    mysqlDiagOk "No error logs"
  fi

  local STARTED=false
  if [[ $(wex docker/containerStarted -n=${CONTAINER}) == false ]];then
    mysqlDiagKo "Container stopped"

    docker start ${CONTAINER}

    if [[ $(wex docker/containerStarted -n=${CONTAINER}) == false ]];then
      mysqlDiagKo "Failed to restart"
    else
      mysqlDiagOk "Container restarted"
      STARTED=true
    fi
  else
    mysqlDiagOk "Container runs"
    STARTED=true
  fi

  if [ ${STARTED} == true ];then
    local EXEC="docker exec -it ${CONTAINER} mysql "

    if [ -f ./.wex ];then
      if [[ -z ${USER_MYSQL+x} ]];then
        USER_MYSQL='-u '$(wex db/var -n=user)
      fi
      if [[ -z ${PASSWORD+x} ]];then
        PASSWORD=' -p'$(wex db/var -n=password)
      fi
    else
      if [[ -z ${USER_MYSQL+x} ]];then
        USER_MYSQL='-u '$(wex var/get -a="DB username" -r -s -n=USER -d="root")
      fi
      if [[ -z ${PASSWORD+x} ]];then
        PASSWORD=' -p'$(wex var/get -a="DB password" -r -s -n=PASSWORD)
      fi
    fi

    EXEC+=${USER_MYSQL}${PASSWORD}' -s -N -e '

    mysqlDiagOk "Execution method : ${EXEC}"

    local DATABASES=$(${EXEC} "SHOW DATABASES")

    if [[ $(echo -e "${DATABASES}" | grep "Access denied") != "" ]];then
      mysqlDiagKo "${DATABASES} : ${USER_MYSQL} / ${PASSWORD}"
    elif [[ $(echo -e "${DATABASES}" | grep "Unknown database") != "" ]];then
      mysqlDiagKo "Database not found : ${USER_MYSQL} / ${PASSWORD} => "${DATABASES}
    else
      mysqlDiagOk "Database access success"
      echo -e ${DATABASES}

      # From : @lucile-sticky https://github.com/docker-library/mysql/issues/275
      local EXPECTED_USER=$(${EXEC} "SELECT host, user FROM mysql.user WHERE host = '%' AND user = 'root'")
      if [ "${EXPECTED_USER}" == "" ];then
        mysqlDiagKo "Missing 'root'@'%' user access"

        if [[ $(wex prompt/yn -q="Would you like to add 'root'@'%' in mysql.user ?") == true ]];then
          ${EXEC} "CREATE USER 'root'@'%';"
          ${EXEC} "GRANT ALL PRIVILEGES ON * . * TO 'root'@'%'"
          ${EXEC} "FLUSH PRIVILEGES"
        fi
      else
        mysqlDiagOk "All users registered"
      fi
    fi
  fi
}
