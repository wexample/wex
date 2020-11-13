#!/usr/bin/env bash

userList() {
  cut -d: -f1 /etc/passwd
}
