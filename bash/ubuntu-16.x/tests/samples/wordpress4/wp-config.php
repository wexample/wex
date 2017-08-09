<?php

// BEGIN iThemes Security - Do not modify or remove this line
// iThemes Security Config Details: 2
define( 'DISALLOW_FILE_EDIT', true ); // Disable File Editor - Security > Settings > WordPress Tweaks > File Editor
// END iThemes Security - Do not modify or remove this line

/** Enable W3 Total Cache Edge Mode */

define('WP_CACHE', true); //Added by WP-Cache Manager
define('W3TC_EDGE_MODE', true); // Added by W3 Total Cache




/**
 * La configuration de base de votre installation WordPress.
 *
 * Ce fichier contient les réglages de configuration suivants : réglages MySQL,
 * préfixe de table, clefs secrètes, langue utilisée, et ABSPATH.
 * Vous pouvez en savoir plus à leur sujet en allant sur
 * {@link http://codex.wordpress.org/fr:Modifier_wp-config.php Modifier
 * wp-config.php}. C'est votre hébergeur qui doit vous donner vos
 * codes MySQL.
 *
 * Ce fichier est utilisé par le script de création de wp-config.php pendant
 * le processus d'installation. Vous n'avez pas à utiliser le site web, vous
 * pouvez simplement renommer ce fichier en "wp-config.php" et remplir les
 * valeurs.
 *
 * @package WordPress
 */

// ** Réglages MySQL - Votre hébergeur doit vous fournir ces informations. ** //
/** Nom de la base de données de WordPress. */
// //Added by WP-Cache Manager
define( 'WPCACHEHOME', '/var/www/html/wp-content/plugins/wp-super-cache/' ); //Added by WP-Cache Manager
define('DB_NAME', 'mysqlTestDataBase');

/** Utilisateur de la base de données MySQL. */
define('DB_USER', 'mysqlTestUserName');

/** Mot de passe de la base de données MySQL. */
define('DB_PASSWORD', 'mysqlTestPassword');

/** Adresse de l'hébergement MySQL. */
define('DB_HOST', 'wexamplesfdivers.mysql.db');

/** Jeu de caractères à utiliser par la base de données lors de la création des tables. */
define('DB_CHARSET', 'utf8mb4');

/** Type de collation de la base de données.
 * N'y touchez que si vous savez ce que vous faites.
 */
define('DB_COLLATE', '');

/**#@+
 * Clefs uniques d'authentification et salage.
 *
 * Remplacez les valeurs par défaut par des phrases uniques !
 * Vous pouvez générer des phrases aléatoires en utilisant
 * {@link https://api.wordpress.org/secret-key/1.1/salt/ le service de clefs secrètes de WordPress.org}.
 * Vous pouvez modifier ces phrases à n'importe quel moment, afin d'invalider tous les cookies existants.
 * Cela forcera également tous les utilisateurs à se reconnecter.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '#,]O/-:*`i9&+wu8.$bog@!OUpcF-H5_~yF8dgosHJeeWcbQ@R4>X3i@WB)~=sfb');
define('SECURE_AUTH_KEY',  '+R{-b#AwTT*B>hh2<IM|HFtOuOuJ5n#AQ!k&Qo3ckR3NPX-Ps&)Fl!F]+csV]y;n');
define('LOGGED_IN_KEY',    'dzUHF-~T7IqhoT: !-|<&]0MJJW)Q1[xAEsG<^lG_+=NQreI?sOoFg^r:%QF}ZrN');
define('NONCE_KEY',        'm;]SuK#|a E;3df|`%_!3tRe$|.E~S#Wa)B4!B9s^Qq1j#H<^DSZO3pH6W<)(}|$');
define('AUTH_SALT',        'lj5.feI6Vi86:E$c)X*|wjCtz`U[M>G4wl).PyV)~uhUE--<7|>c`Ce|C-,05Me0');
define('SECURE_AUTH_SALT', 'S~Q1d.LK(/Gr?-L:w}sZ4r@}>L(8r*7nQA?Lhk(y@:<PjrV!SGj4eu;x%2F$nN!y');
define('LOGGED_IN_SALT',   '9*a/=g,c)?5tDVbR0 Jp[CI7r|,m4-gGZ->D~d~+J]7B:d-1kHYa-|bkY*@L0Q]_');
define('NONCE_SALT',       'A24q9+&Zura2m6{&D0X}i-K7)//{kn(lVsIA>cD1mfq/T&+dbCD|>q<8H_wxHfxJ');
/**#@-*/

/**
 * Préfixe de base de données pour les tables de WordPress.
 *
 * Vous pouvez installer plusieurs WordPress sur une seule base de données
 * si vous leur donnez chacune un préfixe unique.
 * N'utilisez que des chiffres, des lettres non-accentuées, et des caractères soulignés!
 */
$table_prefix  = 'wp_anarchy';

/**
 * Pour les développeurs : le mode deboguage de WordPress.
 *
 * En passant la valeur suivante à "true", vous activez l'affichage des
 * notifications d'erreurs pendant votre essais.
 * Il est fortemment recommandé que les développeurs d'extensions et
 * de thèmes se servent de WP_DEBUG dans leur environnement de
 * développement.
 */
define('WP_DEBUG', false);

/* C'est tout, ne touchez pas à ce qui suit ! Bon blogging ! */

/** Chemin absolu vers le dossier de WordPress. */
if ( !defined('ABSPATH') )
    define('ABSPATH', dirname(__FILE__) . '/');

/** Réglage des variables de WordPress et de ses fichiers inclus. */
//require_once(ABSPATH . 'wp-settings.php');
