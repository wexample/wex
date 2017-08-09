<?php

// Get path as first option.
$settingFile = $argv[1];

require $settingFile;

echo ('WEBSITE_SETTINGS_DATABASE="' . $databases['default']['default']['database'] . '"; ');
echo ('WEBSITE_SETTINGS_USERNAME="' . $databases['default']['default']['username'] . '"; ');
echo ('WEBSITE_SETTINGS_PASSWORD="' . $databases['default']['default']['password'] . '"; ');
