#!/usr/bin/env bash

stringHash() {
  date +%s | sha256sum | base64 | head -c 32 ; echo
}