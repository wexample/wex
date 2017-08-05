#!/usr/bin/env bash

fileGetLastFilledLine() {
 echo $(awk '/./{line=$0} END{print line}' ${1})
}
