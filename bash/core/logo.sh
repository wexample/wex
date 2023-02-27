#!/usr/bin/env bash

coreLogoArgs() {
  _DESCRIPTION="Display wex logo"
}

coreLogo() {
  if [ "${QUIET}" = "true" ]; then
    return
  fi

  local RED='\033[1;91m'
  local NC='\033[0m'

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
}
