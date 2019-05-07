<?php

# Default Wordpress configuration, should not be changed
# until a new version of WP is used, except to make variable editable
# from container configuration.

# Load passed env variables.
$env = parse_ini_file(dirname(__FILE__) . '/../tmp/php.env.ini');

/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', $env['MYSQL_DB_NAME']);

/** MySQL database username */
define('DB_USER', $env['MYSQL_DB_USER']);

/** MySQL database password */
define('DB_PASSWORD', $env['MYSQL_DB_PASSWORD']);

/** MySQL hostname */
define('DB_HOST', $env['MYSQL_DB_HOST']);

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', isset($env['WP_DB_CHARSET']) ? $env['WP_DB_CHARSET'] : 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', isset($env['WP_DB_COLLATE']) ? $env['WP_DB_COLLATE'] : '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '995e50a4050b65ef3c087f480d8e48fba7d98411');
define('SECURE_AUTH_KEY',  '950b92081ca351b8f2be607eaa4d43c3f7c29d3d');
define('LOGGED_IN_KEY',    '05bc3119cc3241bcefd979dad22650bd4856436d');
define('NONCE_KEY',        'f65ac35f84a37faae73bc18d0dc63af84b1e26bd');
define('AUTH_SALT',        '00a8388f0b0e27bb01b6d5631977f06b91827e09');
define('SECURE_AUTH_SALT', 'd7f862f93813604064be7d90ee76563fbaa1f817');
define('LOGGED_IN_SALT',   '8fdfc917d2effe4e3ccdb84cf7dfed1d696bdf8b');
define('NONCE_SALT',       'd033cf1d05e7be0264280bc170e3ae63be21047d');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = isset($env['WP_DB_TABLE_PREFIX']) ? $env['WP_DB_TABLE_PREFIX'] : '';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

// If we're behind a proxy server and using HTTPS, we need to alert Wordpress of that fact
// see also http://codex.wordpress.org/Administration_Over_SSL#Using_a_Reverse_Proxy
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
    define('ABSPATH', dirname(__FILE__) . '/');

# Wex common configuration
# No core auto update.
define('WP_AUTO_UPDATE_CORE', false);
# No core / plugins update
define('DISALLOW_FILE_MODS', true);
# Load custom wex configuration.
require_once dirname(__FILE__) . '/wp-content/config/wp-config.php';

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');

# Protect against wp-cli execution.
if (function_exists('register_theme_directory')) {
    # Add wex theme child dir (versioned).
    register_theme_directory($dir_current . 'wp-content/themes-child');
}

