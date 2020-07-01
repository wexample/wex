#!/usr/bin/env bash

coreLogo() {
  RED='\033[1;91m'
  WHITE='\033[0;30m'
  NC='\033[0m'

  # Conbgfbdfgtinued from above example
  echo -e "${RED}"

  echo ""
  echo ""
  echo "                        .o%%%o."
  echo "                    .%%%%%%%%%%%%%%."
  echo "               .&&&%%%%%%%%%%%%%%%%%%%%%."
  echo "            &&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%"
  echo "           &&&&&&/    %%%%%%%%%%%%   \\%%%%%%%"
  echo "           &&&&&&     %%%%%%%%%%%%     %%%%%%"
  echo "           &&&&&&     &&&&&%%%%%%%     %%%%%%"
  echo "           &&&&&&     &&&\`    \`&&&     %%&&&&"
  echo "           &&&&&&./&                &\\.&&&&&&"
  echo "           &&&&&&&&@      .&&.      &&&&&&&&&"
  echo "            &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
  echo "               \`&&&&&&&&&&&&&&&&&&&&&&&&\`"
  echo "                    \`&&&&&&&&&&&&&&\`"
  echo "                        \`°&&&&°\`"

  echo -e "${NC}" \ "            "
  echo "                  .-..-..-. .--. .-.,-. "
  echo "                  : \`; \`; :' '_.'\`.  .'"
  echo "                  \`.__.__.'\`.__.':_,._;"
  echo "                   ★ www.wexample.com ★"
  echo "                          v${WEX_CORE_VERSION}"
  echo ""
  echo ""

  # Extra message is set.
  if [ ! -z "${1+x}" ]; then
    echo "       ~> ${1}";
  fi;
}
