<?php

$composerJsonPath = $argv[1];

$composerJson = json_decode(file_get_contents($composerJsonPath));

$silex            = "silex/silex";
$symfony          = "symfony/symfony";
$framework = false;

if (isset($composerJson->require->$silex)) {
    $framework = 'silex'.
      // Get version number without special chars
      (str_replace(
        ['~', '^'],
        '',
        explode('.', $composerJson->require->$silex)[0]
      ));
} else if (isset($composerJson->require->$symfony)) {
    $framework = 'symfony'.
      // Get version number without special chars
      (str_replace(
        ['~', '^'],
        '',
        explode('.', $composerJson->require->$symfony)[0]
      ));
}

if ($framework) {
    echo 'WEBSITE_FRAMEWORK="'.$framework.'";';
}
