<?php

function htaccessGetEnv($htaccessPath, $envName)
{
    $htaccess = file($htaccessPath);
    foreach ($htaccess as $line) {
        if (preg_match(
          '/^\s*SetEnv\s+'.$envName.'\s+(.*?)\s*$/',
          trim($line),
          $matches
        )) {
            return $matches[1];
        }
    }
}

