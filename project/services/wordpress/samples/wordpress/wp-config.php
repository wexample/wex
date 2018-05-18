<?php

/**
 * This file is mounted as wp-config.wex.php
 */

# For BackUpWordpress plugin.
define( 'HMBKP_PATH', '/var/www/html/wp-content/backups' );

$site_env = strtolower(getenv('WEX_SITE_ENV'));
$env_config = dirname(__FILE__) . 'docker-compose.' . $site_env . '.php';

if (file_exists($env_config)) {
    require_once $env_config;
}