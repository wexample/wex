#!/usr/bin/env bash

serviceInstallArgs() {
  _ARGUMENTS=(
    [0]='service s "Service to install" true',
    [1]='git g "Init git repository" false',
  )
}

serviceInstall() {
  local SERVICE_SAMPLE_DIR=${WEX_DIR_SAMPLES}"services/"${SERVICE}"/"
  local DIR_SITE=./
echo "" # TODO TEMP

  # Copy all files from samples
  if [ -d ${SERVICE_SAMPLE_DIR} ] && [ ! -d ${DIR_SITE}${SERVICE} ];then
    local FILES=$(ls -a ${SERVICE_SAMPLE_DIR})
    for FILE in ${FILES[@]};do
      if [ "${FILE}" != "." ] && [ "${FILE}" != ".." ];then
        # Docker files
        if [ "${FILE}" == "docker" ] && [ -d "${SERVICE_SAMPLE_DIR}${FILE}" ];then
          # Merge default yml
          serviceInstallMergeYml "yml"
          # Fore each env type.
          local ENV
          for ENV in ${WEX_WEXAMPLE_ENVIRONMENTS[@]};do
            # Search for *.envName.yml
            serviceInstallMergeYml ${ENV}".yml"
          done
        # Git
        elif [ "${FILE}" == ".gitignore.source" ];then
          if [ "${GIT}" == true ];then
            echo -e "" >> ${DIR_SITE}".gitignore"
            cat ${SERVICE_SAMPLE_DIR}${FILE} >> ${DIR_SITE}".gitignore"
          fi
        else
          cp -n -R ${SERVICE_SAMPLE_DIR}${FILE} ${DIR_SITE}${FILE}
        fi
      fi
    done
  fi
}

serviceInstallMergeYml() {
  local EXT=${1}
  local YML_SOURCE_BASE=${SERVICE_SAMPLE_DIR}"docker/docker-compose"
  local YML_SOURCE_FILE=${YML_SOURCE_BASE}"."${EXT}
  local YML_DEST_FILE=${DIR_SITE}"docker/docker-compose."${EXT}
  local YML_CONTENT=''

  if [ -f ${YML_SOURCE_FILE} ];then
    local YML_FILES_TO_MERGE=(${YML_SOURCE_FILE})
    YML_FILES_TO_MERGE+=($(ls ${YML_SOURCE_BASE}-* 2>/dev/null))

    local FILE_TO_MERGE
    for FILE_TO_MERGE in ${YML_FILES_TO_MERGE[@]};do
      # Report suffixes to service name.
      local SUFFIX=''
      local FILENAME=$(basename ${FILE_TO_MERGE})
      if [[ ${#FILENAME} > 18 ]];then
        SUFFIX="_"${FILENAME:15:-4}
      fi

      # Append
      YML_CONTENT+="    "${SITE_NAME}"_"${SERVICE}${SUFFIX}":\n"
      YML_CONTENT+=$(cat ${FILE_TO_MERGE})"\n"
    done
  fi

  if [ "${YML_CONTENT}" != "" ];then
      # Create file if not exists.
      if [ ! -f ${YML_DEST_FILE} ];then
        echo -e "version: '2'\n\nservices:" > ${YML_DEST_FILE}
      fi
      # Append to yml file
      echo -e "${YML_CONTENT}" > ${YML_DEST_FILE}.tmp
      sed -i "/services:/r ${YML_DEST_FILE}.tmp" ${YML_DEST_FILE}
  fi
}