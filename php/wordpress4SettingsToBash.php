<?php

// Get path as first option.
$settingFile = $argv[1];

require $settingFile;

echo('WEBSITE_SETTINGS_HOST="'.DB_HOST.'"; ');
if (defined('DB_PORT')) {
    echo('WEBSITE_SETTINGS_PORT="'.DB_PORT.'"; ');
}
echo('WEBSITE_SETTINGS_DATABASE="'.DB_NAME.'"; ');
echo('WEBSITE_SETTINGS_USERNAME="'.DB_USER.'"; ');
echo('WEBSITE_SETTINGS_PASSWORD="'.DB_PASSWORD.'"; ');
