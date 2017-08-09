<?php

// Get JSON config path.
$settingFile = $argv[1];
$env         = isset($argv[2]) ? $argv[2] : false;

$value = json_decode(file_get_contents($settingFile));

// Get the first given env key.
if (!$env) {
    $env = key($value->config);
}

echo('WEBSITE_SETTINGS_DATABASE="'.$value->config->$env->database->dbname.'"; ');
echo('WEBSITE_SETTINGS_USERNAME="'.$value->config->$env->database->user.'"; ');
echo('WEBSITE_SETTINGS_PASSWORD="'.$value->config->$env->database->password.'"; ');
