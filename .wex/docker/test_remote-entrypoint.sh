#!/bin/bash

cp /opt/wex/.wex/.env.test_remote /opt/wex/.wex/.env

bash /opt/wex/cli/install

# Delete old test proxy
docker rm -f wex_proxy_test_remote_proxy
rm -rf /var/www/test_remote/wex-proxy

# Start local proxy
wex app::helper/start -n proxy -p 3337 -ps 3338

/usr/sbin/sshd -D
