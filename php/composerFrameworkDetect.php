<?php

$composerJsonPath = $argv[1];

$composerJson = json_decode(file_get_contents($composerJsonPath));

$silex            = "silex/silex";
$symfony          = "symfony/symfony";
$websiteFramework = false;

if (isset($composerJson->require->$silex)) {
    $websiteFramework = 'silex'.
      // Get version number without special chars
      (str_replace(
        ['~', '^'],
        '',
        explode('.', $composerJson->require->$silex)[0]
      ));
} else if (isset($composerJson->require->$symfony)) {
    $websiteFramework = 'symfony'.
      // Get version number without special chars
      (str_replace(
        ['~', '^'],
        '',
        explode('.', $composerJson->require->$symfony)[0]
      ));
}

if ($websiteFramework) {
    echo 'WEBSITE_FRAMEWORK="'.$websiteFramework.'";';
}
