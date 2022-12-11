#!/usr/bin/env bash

mysqlTest() {
  wexTestAssertEqual $(wex file/lineExists -f=".gitignore" -l="/dumps/*") true
}
