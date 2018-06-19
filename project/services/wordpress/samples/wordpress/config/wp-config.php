<?php

/**
 * This file is mounted as wp-config.wex.php
 */

$dir_current = dirname(__FILE__) . '/../../';

# For BackUpWordpress plugin.
define('HMBKP_PATH', $dir_current . 'wp-content/backups');

$site_env = strtolower(getenv('WEX_SITE_ENV'));
$env_config = $dir_current . 'wp-config.' . $site_env . '.php';

if (file_exists($env_config)) {
    require_once $env_config;
}