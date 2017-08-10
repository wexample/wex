#!/usr/bin/env bash

frameworkGetEnvironment() {
  # Detect type.
  websiteType=$(wexample frameworkDetect ${1});
  # Parse file.
  wexample ${websiteType}'Environment' ${1}
}
