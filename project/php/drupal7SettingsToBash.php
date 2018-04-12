<?php

// Get path as first option.
$settingFile = $argv[1];

@require $settingFile;

echo ('SITE_DB_HOST="' . $databases['default']['default']['host'] . '"; ');
echo ('SITE_DB_PORT="' . $databases['default']['default']['port'] . '"; ');
echo ('SITE_DB_NAME="' . $databases['default']['default']['database'] . '"; ');
echo ('SITE_DB_USER="' . $databases['default']['default']['username'] . '"; ');
echo ('SITE_DB_PASSWORD="' . $databases['default']['default']['password'] . '"; ');
