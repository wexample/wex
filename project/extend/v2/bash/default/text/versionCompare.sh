#!/usr/bin/env bash

textVersionCompareArgs() {
  _ARGUMENTS=(
    [0]='version_a a "Version A" true'
    [1]='version_b b "Version B" true'
  )
}

textVersionCompare() {
    if [[ ${VERSION_A} == ${VERSION_B} ]]
    then
        echo '='
        return
    fi
    local IFS=.
    local i ver1=(${VERSION_A}) ver2=(${VERSION_B})
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            echo '>'
            return
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            echo '<'
            return
        fi
    done
    echo '?'
    return
}