#!/bin/bash

# Delete old test proxy
docker rm -f wex_proxy_test_remote_proxy
rm -rf /var/www/test_remote/wex-proxy

# Start local proxy
wex app::helper/start -n proxy -p 3337 -ps 3338

# Mark as ready
touch /test_remote.ready
chmod 777 /test_remote.ready

/usr/sbin/sshd -D
