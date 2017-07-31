<?php

// Get path as first option.
$settingFile = $argv[1];

require $settingFile;

echo ('WEX_DRUPAL_7_SETTINGS_DATABASE="' . $databases['default']['default']['database'] . '"; ');
echo ('WEX_DRUPAL_7_SETTINGS_USERNAME="' . $databases['default']['default']['username'] . '"; ');
echo ('WEX_DRUPAL_7_SETTINGS_PASSWORD="' . $databases['default']['default']['password'] . '"; ');
