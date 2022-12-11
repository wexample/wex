#!/usr/bin/env bash

sonarqubeAppStart() {
  # Wrong files permissions may cause container won't start.
  chmod 777 -R ./sonarqube/
}
