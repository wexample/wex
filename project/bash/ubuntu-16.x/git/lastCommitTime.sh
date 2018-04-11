#!/usr/bin/env bash

gitLastCommitTime() {
  git log -1 --format=%at
}
