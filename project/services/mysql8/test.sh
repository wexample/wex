#!/usr/bin/env bash

mysql8Test() {
  wexTestAssertEqual $(wex file/lineExists -f=".gitignore" -l="/dumps/*") true
}
