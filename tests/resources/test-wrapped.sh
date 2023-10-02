#!/usr/bin/env bash

PROJECT=""
VALUE=""

while (( "$#" )); do
  case "$1" in
    -p)
      PROJECT="$2"
      shift 2
      ;;
    -v)
      VALUE="$2"
      shift 2
      ;;
    -*|--*=)
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *)
      shift
      ;;
  esac
done

echo "PROJECT: $PROJECT"
echo "VALUE: $VALUE"