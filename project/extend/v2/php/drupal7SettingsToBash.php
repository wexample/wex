<?php

// Get path as first option.
$settingFile = $argv[1];

@require $settingFile;

echo ('MYSQL_DB_HOST="' . $databases['default']['default']['host'] . '"; ');
echo ('MYSQL_DB_PORT="' . $databases['default']['default']['port'] . '"; ');
echo ('MYSQL_DB_NAME="' . $databases['default']['default']['database'] . '"; ');
echo ('MYSQL_DB_USER="' . $databases['default']['default']['username'] . '"; ');
echo ('MYSQL_DB_PASSWORD="' . $databases['default']['default']['password'] . '"; ');
