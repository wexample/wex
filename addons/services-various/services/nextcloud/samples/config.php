<?php

$CONFIG = [
    // Update files at each access to keep updated list.
    'filesystem_check_changes' => 1,
    // Avoid a lot of file locking errors.
    'filelocking.enabled' => false,
    // Trash management policy.
    'trashbin_retention_obligation' => 'auto, 1',
];
