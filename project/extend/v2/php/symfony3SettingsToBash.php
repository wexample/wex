<?php

require_once dirname(__FILE__)."/../vendor/autoload.php";

use Symfony\Component\Yaml\Yaml;

// Get YAML path.
$settingFile = $argv[1];

$value = Yaml::parse(file_get_contents($settingFile));

// Prevent "null" string.
$port = $value['parameters']['database_port'];
$port = $port !== 'null' ? $port : '';

echo('MYSQL_DB_HOST="'.$value['parameters']['database_host'].'"; ');
echo('MYSQL_DB_PORT="'.$port.'"; ');
echo('MYSQL_DB_NAME="'.$value['parameters']['database_name'].'"; ');
echo('MYSQL_DB_USER="'.$value['parameters']['database_user'].'"; ');
echo('MYSQL_DB_PASSWORD="'.$value['parameters']['database_password'].'"; ');
