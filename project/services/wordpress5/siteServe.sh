#!/usr/bin/env bash

wordpress5SiteServe() {
   # Might be the default way to serve instead of restart.
   wex site/exec -c="service apache2 reload"
}