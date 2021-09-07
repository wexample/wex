#!/usr/bin/env bash

webCodeFormat()  {
  cd './project' || return;
  yarn prettier --write .
  cd '../' || return;

  wex site/exec -l -c="./vendor/bin/php-cs-fixer fix"
}