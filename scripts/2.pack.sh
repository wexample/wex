# 2

cd /var/www/build/workdir/wex_5.0.0~beta.2 || return
sudo chown -R owner:owner ../../

# Only "cli" folder is executable
sudo chmod -R -x wex
sudo chmod -R +x wex/cli
sudo find wex/ -name "*.sh" -type f -exec chmod +x {} \;

# All "folders" have 755 permission
sudo find . -type d -exec chmod 755 {} \;

# Build.
debuild -us -uc

# Sign
cd /var/www/build/workdir/ || return
debsign -k contact@wexample.com wex_5.0.0~beta.2-1_amd64.changes
