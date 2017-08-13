#!/usr/bin/env bash

systemExecRecursive() {
  find . -type f -print0 | xargs -0 $@
}
