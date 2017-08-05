#!/usr/bin/env bash

wexampleLogo() {
  RED='\033[1;91m'
  WHITE='\033[0;30m'
  NC='\033[0m'

  # Continued from above example
  echo -e "${RED}"

  echo "                        m"
  echo "                   .MMMMMMMMM."
  echo "               .######MMKMMMMMMMMM."
  echo "           .8##########M~~MMMMMMMMMMM."
  echo "        .888888#####!|MP~~~|!MMMMMMMMMMM."
  echo '        |~~7888888`  |7~!~~|  `MMMMMMMMM|'
  echo '        |~~~~~7|     |/` `\|     |MMMMMM|'
  echo "        |+~~~~~|                 |#MMMMM|"
  echo "        |+~~~~~|                 |###MMM|"
  echo "        |++~~~~|                 |####MM|"
  echo "        |++++~~~~_     _!_     _#######M|"
  echo "         +++++~~~~~~~.+++++.688888######"
  echo "            +++++~~~~~~~++2288888888#"
  echo "                +++++~~~~22228888"
  echo "                    -+~~~2222"
  echo "                        *"
  echo -e "${NC}" \
        "                                         _"
  echo "                                         | |"
  echo "  __      _______  ____ _ _ __ ___  _ __ | | ___"
  echo "  \ \ /\ / / _ \ \/ / _\` | '_ \` _ \| '_ \| |/ _ \\"
  echo "   \ V  V /  __/>  < (_| | | | | | | |_) | |  __/"
  echo "    \_/\_/ \___/_/\_\__,_|_| |_| |_| .__/|_|\___|"
  echo "     http://network.wexample.com   | |"
  echo "     # Scripts recipe              |_|"
  echo ""

  # Extra message is set.
  if [ ! -z "${1+x}" ]; then
    echo "       ~> ${1}";
  fi;
}
