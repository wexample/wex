<?php

// Get JSON config path.
$settingFile = $argv[1];
$env = $argv[2];

$value = json_decode(file_get_contents($settingFile));

echo('WEX_SILEX_1_SETTINGS_DATABASE="'.$value->config->$env->database->dbname.'"; ');
echo('WEX_SILEX_1_SETTINGS_USERNAME="'.$value->config->$env->database->user.'"; ');
echo('WEX_SILEX_1_SETTINGS_PASSWORD="'.$value->config->$env->database->password.'"; ');
