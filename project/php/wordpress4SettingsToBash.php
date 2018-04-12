<?php

// Get path as first option.
$settingFile = $argv[1];

$dirname = dirname($settingFile);

# wp-settings.php is required by wp-config.php
# So prevent to load it, copy it.
copy($dirname.'/wp-settings.php', $dirname.'/_wp-settings.php');
# Add a commented temp file
file_put_contents(
  $dirname.'/wp-settings.php',
  '<?php // This is a temp file used by wexample to read WP connexion data and prevent site launching.'
);
# Load config.
require $settingFile;
# Revert changes.
copy($dirname.'/_wp-settings.php', $dirname.'/wp-settings.php');
unlink($dirname.'/_wp-settings.php');

echo('SITE_DB_HOST="'.DB_HOST.'"; ');
if (defined('DB_PORT')) {
    echo('SITE_DB_PORT="'.DB_PORT.'"; ');
}
echo('SITE_DB_NAME="'.DB_NAME.'"; ');
echo('SITE_DB_USER="'.DB_USER.'"; ');
echo('SITE_DB_PASSWORD="'.DB_PASSWORD.'"; ');
