#!/bin/bash
# Help menu
print_help() {
cat <<-HELP
Forked by weeger from https://www.drupal.org/node/244924
This script is used to fix permissions of a Drupal installation
you need to provide the following arguments:
1) Path to your Drupal installation.
Usage: bash ${0##*/} --drupal_path=PATH
Example: bash ${0##*/} --drupal_path=/usr/local/apache2/htdocs
HELP
exit 0
}

drupal_path=${1%/}
# Parse Command Line Arguments
while [ $# -gt 0 ]; do
  case "$1" in
    --drupal_path=*)
      drupal_path="${1#*=}"
      ;;
    --help) print_help;;
    *)
      printf "***********************************************************\n"
      printf "* Error: Invalid argument, run --help for valid arguments. *\n"
      printf "***********************************************************\n"
      exit 1
  esac
  shift
done

if [ -z "${drupal_path}" ] || [ ! -d "${drupal_path}/sites" ] || [ ! -f "${drupal_path}/core/modules/system/system.module" ] && [ ! -f "${drupal_path}/modules/system/system.module" ]; then
  printf "*********************************************\n"
  printf "* Error: Please provide a valid Drupal path. *\n"
  printf "*********************************************\n"
  print_help
  exit 1
fi
cd $drupal_path
printf "Changing permissions of all directories inside "${drupal_path}" to "r-xr-x---"...\n"
find . -type d -exec chmod u=rx,g=rx,o=rx '{}' \;
printf "Changing permissions of all files inside "${drupal_path}" to "rw-r---rx"...\n"
find . -type f -exec chmod u=rx,g=r,o=r '{}' \;
printf "Changing permissions of "files" directories in "${drupal_path}/sites" to "rwxrwxr-x"...\n"
cd sites
find . -type d -name files -exec chmod ug=rwx,o=rx '{}' \;
printf "Changing permissions of all files inside all "files" directories in "${drupal_path}/sites" to "rw-rw-r-x"...\n"
printf "Changing permissions of all directories inside all "files" directories in "${drupal_path}/sites" to "rwxrwxr-x"...\n"
for x in ./*/files; do
        find ${x} -type d -exec chmod ug=rwx,o=rx '{}' \;
        find ${x} -type f -exec chmod ug=rwx,o=rx '{}' \;
done

# Go down
cd ../

printf "Changing .htaccess permission to 655\n"
chmod 655 .htaccess

printf "Changing current dir permission to 755\n"
chmod 755 .

echo "Done setting proper permissions on files and directories"
