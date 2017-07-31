<?php

require_once dirname(__FILE__)."/../vendor/autoload.php";

use Symfony\Component\Yaml\Yaml;

// Get YAML path.
$settingFile = $argv[1];

$value = Yaml::parse(file_get_contents($settingFile));

echo('WEX_SYMFONY_3_SETTINGS_DATABASE="'.$value['parameters']['database_name'].'"; ');
echo('WEX_SYMFONY_3_SETTINGS_USERNAME="'.$value['parameters']['database_user'].'"; ');
echo('WEX_SYMFONY_3_SETTINGS_PASSWORD="'.$value['parameters']['database_password'].'"; ');
