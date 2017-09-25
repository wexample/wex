#!/usr/bin/env bash

. ${_TEST_RUN_DIR_CURRENT}"config/comment.sh"

configUncommentTest() {
  configCommentTest $@
}
