#!/usr/bin/env bash

sonarqubeStart() {
  # Wrong files permissions may cause container won't start.
  chmod 777 -R ./sonarqube/
}
