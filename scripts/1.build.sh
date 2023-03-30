#!/usr/bin/env bash

APP_NAME='wex'
VERSION='5.0.0~beta.3'
BUILD_NAME="${APP_NAME}_${VERSION}"
PATH_ROOT="$(realpath "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")/"
PATH_BUILD="${PATH_ROOT}builds/"
PATH_BUILD_BUILD="${PATH_BUILD}${BUILD_NAME}/"
PATH_BUILD_SOURCE="${PATH_BUILD_BUILD}wex"
cd "${PATH_ROOT}" || return

echo "Cleanup build dir for ${BUILD_NAME}"
rm -rf "${PATH_BUILD_SOURCE}"
rm -f "${PATH_BUILD}${BUILD_NAME}.orig.tar.gz"

mkdir -p "${PATH_BUILD_SOURCE}"
cd "${PATH_BUILD_SOURCE}" || return

echo "Cloning la sources to build folder"
git clone "${PATH_ROOT}source/" .

echo "Remove useless files"
rm -rf .git
rm -rf .wex
find . -name ".gitignore" -type f -delete

cd "${PATH_BUILD}" || return
tar -czvf "${BUILD_NAME}.orig.tar.gz" "${BUILD_NAME}/wex"
chown -R owner:owner "${PATH_BUILD}"

echo "Copy debian files"
cp -r "${PATH_ROOT}templates/debian" "${PATH_BUILD_BUILD}"
cp "${PATH_ROOT}templates/wex.1" "${PATH_BUILD_BUILD}"

echo "Build changelog"
python3 "${PATH_ROOT}scripts/1.build.py" -n "${APP_NAME}" -v "${VERSION}"

echo "Done."