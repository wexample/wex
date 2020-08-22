
demoChoice() {
  local ARR=(one two three)
  local SELECTED=1

  renderLine
}

reloadLine() {
  printf "\033[%sA" "${#ARR}"
  printf "\r"

  renderLine
}

renderLine() {
  local COUNTER=0

  for ITEM in "${ARR[@]}"
  do
    ((COUNTER++))
    local COLOR;
    local LINE="\033[K    "

    if [ "${COUNTER}" = "${SELECTED}" ];then
      LINE+="${WEX_COLOR_WHITE}${COUNTER} ${WEX_COLOR_GRAY} > ${WEX_COLOR_YELLOW}\033[1m"
    else
      LINE+="${WEX_COLOR_GRAY}${COUNTER} > ${WEX_COLOR_RESET}"
    fi

    printf "${LINE}%s\n" "${ITEM}"
  done;

  printf "%b" "${WEX_COLOR_CYAN}"

  local ESCAPE
  ESCAPE=$(printf "\u1b")

  read -rsn 1 -p "$(echo -e "Select what you want: ${WEX_COLOR_RESET}")" ARROW
  if [ "${ARROW}" = "${ESCAPE}" ]; then
      read -rsn2 ARROW # read 2 more chars
  fi
  case "${ARROW}" in
      '[A')
        ((SELECTED--))

        if [ ${SELECTED} -le 0 ];then
          SELECTED=0
        fi

        reloadLine ;;
      '[B')
        ((SELECTED++))

        if [ ${SELECTED} -ge ${#ARR} ];then
          SELECTED=${#ARR}
        fi

        reloadLine ;;
      # TODO
      *) >&2 echo 'ERR bad input'; return ;;
  esac
}