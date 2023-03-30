#!/usr/bin/env bash

VERSION="wex_5.0.0~beta.3"
PATH_ROOT="$(realpath "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")/"
PATH_BUILD="${PATH_ROOT}builds/"
PATH_BUILD_SOURCE="${PATH_BUILD}${VERSION}/wex"
cd "${PATH_ROOT}" || return

echo "Cleanup build dir for ${VERSION}"
rm -rf "${PATH_BUILD_SOURCE}"
rm -f "${PATH_BUILD}${VERSION}.orig.tar.gz"

mkdir -p "${PATH_BUILD_SOURCE}"
cd "${PATH_BUILD_SOURCE}" || return

echo "Cloning la sources to build folder"
git clone "${PATH_ROOT}source/" .

echo "Remove useless files"
rm -rf .git
rm -rf .wex
find . -name ".gitignore" -type f -delete


cd "${PATH_BUILD}" || return
tar -czvf "${VERSION}.orig.tar.gz" "${VERSION}/wex"
chown -R owner:owner .

echo "Done."