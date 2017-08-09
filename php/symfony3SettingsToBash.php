<?php

require_once dirname(__FILE__)."/../vendor/autoload.php";

use Symfony\Component\Yaml\Yaml;

// Get YAML path.
$settingFile = $argv[1];

$value = Yaml::parse(file_get_contents($settingFile));

echo('WEBSITE_SETTINGS_DATABASE="'.$value['parameters']['database_name'].'"; ');
echo('WEBSITE_SETTINGS_USERNAME="'.$value['parameters']['database_user'].'"; ');
echo('WEBSITE_SETTINGS_PASSWORD="'.$value['parameters']['database_password'].'"; ');
