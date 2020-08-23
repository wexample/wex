
demoChoice() {
  local ARR=(one two three a b c d e f g h i j k l m n o p q r s t u v etc)

  choice
}

choice() {
  local SELECTED=0

  renderLine
}

reloadLine() {
  # Move cursor up
  printf "\033[%sA" "${#ARR[@]}"

  printf "\r"

  renderLine
}

renderLine() {
  local COUNTER=0

  for ITEM in "${ARR[@]}"
  do
    ((COUNTER++))
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

  local BACKSPACE=$(cat << eof
0000000 005177
0000002
eof
)

  local SELECTED_DISPLAY=${SELECTED}
  # Hide zero from display
  if [ "${SELECTED}" = "0" ];then
    SELECTED_DISPLAY=""
  fi

  read -rsn 1 -p "$(echo -e "Select what you want: ${WEX_COLOR_RESET}${SELECTED_DISPLAY}   ")" ARROW

  if [ "$(echo "$ARROW" | od)" = "${BACKSPACE}" ];then
    SELECTED=${SELECTED%?}
    reloadLine
  fi

  if [ "${ARROW}" = "${ESCAPE}" ]; then
      read -rsn 2 ARROW # read 2 more chars
  fi
  case ${ARROW} in
      '[A')
        ((SELECTED--))

        if [ ${SELECTED} -le 0 ];then
          SELECTED=0
        fi

        reloadLine ;;
      '[B')
        ((SELECTED++))

        if [ ${SELECTED} -ge ${#ARR[@]} ];then
          SELECTED=${#ARR[@]}
        fi

        reloadLine ;;
      ''|*[0-9]*)
          if [ "${SELECTED}" = "0" ];then
            SELECTED=""
          fi

          SELECTED+=${ARROW}

          if [ "${SELECTED}" -ge $(( ${#ARR[@]} + 1 )) ];then
            SELECTED=0
          fi

          reloadLine
          ;;
#      *) >&2 echo 'ERR bad input'; return ;;
  esac
}