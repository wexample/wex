# 3
# In the repo container

aptly repo create wex
aptly repo add wex /opt/aptly/tmp/workdir/wex_5.0.0~beta.2-1_all.deb
aptly snapshot create wex-snapshot from repo wex
aptly publish snapshot -gpg-key=contact@wexample.com -distribution=beta wex-snapshot
cp /root/.gnupg/public.key /var/www/public