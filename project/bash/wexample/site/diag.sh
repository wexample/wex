#!/usr/bin/env bash

siteDiagOk() {
  local GREEN='\033[1;32m'
  local NC='\033[0m'
  echo -e "${GREEN}OK${NC} "${1}
}

siteDiagKo() {
  local RED="\033[0;31m"
  local NC='\033[0m'
  echo -e "${RED}OK${NC} "${1}
}

siteDiag() {

}