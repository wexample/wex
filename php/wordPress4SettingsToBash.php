<?php

// Get path as first option.
$settingFile = $argv[1];

require $settingFile;

echo ('WEX_WORDPRESS_4_SETTINGS_DATABASE="' . DB_NAME . '"; ');
echo ('WEX_WORDPRESS_4_SETTINGS_USERNAME="' . DB_USER . '"; ');
echo ('WEX_WORDPRESS_4_SETTINGS_PASSWORD="' . DB_PASSWORD . '"; ');
