<?php

// Get arguments from bash.
$args = $argv;
// Ignore first.
array_shift($args);
// Second is function name.
$functionName = array_shift($args);
// Get file (it should contain a function).
require_once $functionName.'.php';
// Execute.
echo call_user_func_array($functionName, $args);
