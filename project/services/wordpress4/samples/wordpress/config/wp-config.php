<?php

/**
 * This file is mounted as wp-config.wex.php
 */

$dir_current = dirname(__FILE__) . '/../../';

# Load passed env variables.
$env = parse_ini_file($dir_current . '/../tmp/php.env.ini');

# For BackUpWordpress plugin.
define('HMBKP_PATH', $dir_current . 'wp-content/backups');

$env_config = $dir_current . 'wp-content/config/wp-config.' . $env['SITE_ENV'] . '.php';

if (file_exists($env_config)) {
    require_once $env_config;
}