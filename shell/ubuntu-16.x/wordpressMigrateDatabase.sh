# TODO Non executable script /!\
# TODO Merge with V2 -> IF EXISTS seems to not be compatible with all version of MySQL.
# TODO Do not ask for old url / db name / db passwork : go to wp-config.php to connect and request wp_options.
# TODO Manage also tables prefixes.

exit

# Migrate a Wordpress database

read -p "Old URL (ex: http://www.oldurl.com) : " old_url
read -p "New URL (ex: http://www.newurl.com) : " new_url
read -p "Database name : " db_name

mysql --user="root" -p --database="$database" --execute="
USE $db_name;
IF EXISTS (select 1 from wp_options LIMIT 0,1) THEN
   UPDATE wp_options SET option_value = replace(option_value, '$old_url', '$new_url') WHERE option_name = 'home' OR option_name = 'siteurl';
END IF;
IF EXISTS (select 1 from wp_posts LIMIT 0,1) THEN
  UPDATE wp_posts SET guid = replace(guid, '$old_url', '$new_url');
  UPDATE wp_posts SET post_content = replace(post_content, '$old_url', '$new_url');
END IF;
IF EXISTS (select 1 from wp_postmeta LIMIT 0,1) THEN
  UPDATE wp_postmeta SET meta_value = replace(meta_value, '$old_url', '$new_url');"
END IF;

# TODO This is another version -----

# Migrate a Wordpress database

read -p "Old URL (ex: http://www.oldurl.com) : " old_url
read -p "New URL (ex: http://www.newurl.com) : " new_url
read -p "Database name : " db_name

mysql --user="root" -p --database="$db_name" --execute="

USE $db_name;

  UPDATE wex_options SET option_value = replace(option_value, '$old_url', '$new_url') WHERE option_name = 'home' OR option_name = 'siteurl';
  UPDATE wex_posts SET guid = REPLACE (guid, '$old_url', '$new_url');
  UPDATE wex_posts SET post_content = REPLACE (post_content, '$old_url', '$new_url');
  UPDATE wex_postmeta SET meta_value = REPLACE (meta_value, '$old_url','$new_url');

"

echo "Complete";
