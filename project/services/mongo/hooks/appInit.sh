#!/usr/bin/env bash

mongoAppInit() {
  wex app/start -c=mongo

  _wexLog "Wait 20 seconds for database fill.."

  wex app/stop
}
