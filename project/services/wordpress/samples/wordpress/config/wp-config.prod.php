<?php

/**
 * This file is mounted as wp-config.wex.php
 */

# For BackUpWordpress plugin.
define('HMBKP_PATH', '/var/www/html/wp-content/backups');

define('WP_ALLOW_MULTISITE', true);
define('MULTISITE', true);
define('SUBDOMAIN_INSTALL', false);
define('DOMAIN_CURRENT_SITE', getenv('WP_DOMAIN_CURRENT_SITE'));
define('PATH_CURRENT_SITE', '/');
define('SITE_ID_CURRENT_SITE', 1);
define('BLOG_ID_CURRENT_SITE', 1);

