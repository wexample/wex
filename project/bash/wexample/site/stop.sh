#!/usr/bin/env bash

siteStop() {
  wex site/compose -c="down"
  # Add site
  wex server/siteRemove -d="./"
  # Write config file
  wex site/configWrite -s=false
}
