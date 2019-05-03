#!/usr/bin/env bash

webCodeFormat()  {
  wex site/exec -l -c="./vendor/bin/php-cs-fixer fix --config ./.php_cs.dist"
}