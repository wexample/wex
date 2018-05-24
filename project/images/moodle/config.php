<?php // Moodle configuration file

# Load passed wex env variables.
$env = parse_ini_file(dirname(__FILE__) . '/../tmp/php.env.ini');

unset($CFG);
global $CFG;
$CFG = new stdClass();

$CFG->dbtype = 'mysqli';
$CFG->dblibrary = 'native';
$CFG->dbhost = $env['MYSQL_DB_HOST'];
$CFG->dbname = $env['MYSQL_DB_NAME'];
$CFG->dbuser = $env['MYSQL_DB_USER'];
$CFG->dbpass = $env['MYSQL_DB_PASSWORD'];
$CFG->prefix = '';
$CFG->dboptions = array(
    'dbpersist' => 0,
    'dbport' => 3306,
    'dbsocket' => '',
    'dbcollation' => 'utf8mb4_unicode_ci',
);

$CFG->wwwroot = 'http' . (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off' ? 's' : '')
    . '://' . $env['DOMAIN_MAIN'];
$CFG->dataroot = '/var/www/html/moodledata';
$CFG->admin = 'admin';

$CFG->directorypermissions = 0777;

require_once(__DIR__ . '/lib/setup.php');

// There is no php closing tag in this file,
// it is intentional because it prevents trailing whitespace problems!
