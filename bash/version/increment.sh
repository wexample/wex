#!/usr/bin/env bash

versionIncrementArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Upgrade version number"
  _ARGUMENTS=(
    'type t "Upgrade type (major, intermediate or minor)" false minor'
    'increment i "Amount of version to increment" false 1'
    'version v "Actual version number" true'
  )
}

versionIncrement() {
  local BUILD
  local MAJOR
  local MINOR

  MAJOR=$(echo "${VERSION}" | cut -d '.' -f 1)
  MINOR=$(echo "${VERSION}" | cut -d '.' -f 2)
  BUILD=$(echo "${VERSION}" | cut -d '.' -f 3)

  # Incrémente selon le type.
  case "${TYPE}" in
    major)
      MAJOR=$((MAJOR + INCREMENT))
      MINOR=0
      BUILD=0
      ;;
    intermediate)
      MINOR=$((MINOR + INCREMENT))
      BUILD=0
      ;;
    minor)
      BUILD=$((BUILD + INCREMENT))
      ;;
    *)
      _wexError "Invalid upgrade type. Choose 'major', 'intermediate' or 'minor'." >&2
      exit 1
      ;;
  esac

  # Vérifie si le résultat est négatif, le met à zéro.
  if [ $MAJOR -lt 0 ]; then
    MAJOR=0
    MINOR=0
    BUILD=0
  elif [ $MINOR -lt 0 ]; then
    MINOR=0
    BUILD=0
  elif [ $BUILD -lt 0 ]; then
    BUILD=0
  fi

  echo "${MAJOR}.${MINOR}.${BUILD}"
}
