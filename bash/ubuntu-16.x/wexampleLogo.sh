#!/usr/bin/env bash

wexampleLogo() {
  RED='\033[1;91m'
  WHITE='\033[0;30m'
  NC='\033[0m'

  # Conbgfbdfgtinued from above example
  echo -e "${RED}"

  echo "                        m"
  echo "                   .#########."
  echo "               .888888##K#########."
  echo "           .68888888888#~~###########."
  echo "        .66666688888!|#P~~~|!###########."
  echo '        |~~7666666`  |7~!~~|  `#########|'
  echo '        |~~~~~7|     |/` `\|     |######|'
  echo "        |+~~~~~|                 |8#####|"
  echo "        |+~~~~~|                 |888###|"
  echo "        |++~~~~|                 |8888##|"
  echo "        |++++~~~~_     _!_     _8888888#|"
  echo "         +++++~~~~~~~.+++++.666666888888"
  echo "            +++++~~~~~~~++22666666668"
  echo "                +++++~~~~22226666"
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
