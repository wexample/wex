#!/usr/bin/env bash

# TODO Detect login / pass for WP / Drupal / Sy
# TODO Prevent trying to do it without a secured ssh connexion (or with a password)
# TODO We can extract all bash commands made in SSH : it can also be used in local
# TODO We may also create remoteConnect / remoteDisconnect methods.

# TODO Make a generic function to read if not exists ?
if [ -z ${host+x} ]; then read -p "Host : " host; fi
if [ -z ${user+x} ]; then read -p "User : " user; fi
if [ -z ${port+x} ]; then read -p "Port : " port; fi

if [ -z ${remote_db_name+x} ]; then read -p "Remote DB Name : " remote_db_name; fi
if [ -z ${remote_db_user+x} ]; then read -p "Remote DB User : " remote_db_user; fi
if [ -z ${remote_db_password+x} ]; then read -p "Remote DB User : " remote_db_password; fi

if [ -z ${local_db_name+x} ]; then read -p "Local DB Name : " local_db_name; fi
if [ -z ${local_db_user+x} ]; then read -p "Local DB User : " local_db_user; fi
if [ -z ${local_db_password+x} ]; then read -p "Local DB User : " local_db_password; fi

dump_file_name="networkV2Dump.sql"
dump_remote_location="/var/www/"
dump_local_location="/var/www/"

# Execute remote command
ssh ${user}@${host} -p ${port} << EOF

su

cd /var/www/

rm -rf networkV2Dump.sql

mysqldump -u${local_db_user} -p${remote_db_password} ${remote_db_name} > "${dump_remote_location}${dump_file_name}"

# Exit root
exit
# Exit SSH
exit

EOF

echo "Get file from ${user}@${host}:${dump_local_location}${dump_file_name} to ${dump_remote_location}${dump_file_name}"
scp -P ${port} ${user}@${host}:"${dump_local_location}${dump_file_name}" "${dump_remote_location}${dump_file_name}"

mysql -u${local_db_user} -p${local_db_password} -e "drop database if exists network_v1; create database network_v1"

mysql -u${local_db_user} -p${local_db_password} ${local_db_name} < ${dump_file_name}

rm -rf ${dump_file_name}



