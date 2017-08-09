<?php

$phpWebsitePath   = $argv[1];
$websiteFramework = false;

if (is_file($phpWebsitePath.'/wp-config.php')) {
    // Wordpress.
    require $phpWebsitePath.'/wp-includes/version.php';
    $websiteFramework = 'wordpress'.(explode('.', $wp_version)[0]);
}
else if (is_file($phpWebsitePath.'/sites/default/settings.php') && is_file($phpWebsitePath.'/includes/bootstrap.inc')) {
    // Drupal.
    require $phpWebsitePath.'/includes/bootstrap.inc';
    $websiteFramework = 'drupal'.(explode('.', VERSION)[0]);
}

if ($websiteFramework) {
    echo 'WEBSITE_FRAMEWORK="'.$websiteFramework.'";';
} else {
    $argv[1] = $phpWebsitePath.'/composer.json';
    # Parse composer.json file.
    # The script manage echo
    require "composerFrameworkDetect.php";
}


