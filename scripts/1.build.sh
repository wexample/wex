# 1
# Le répertoire est monté dans le container wex

cd /var/www/build/ || return
rm -rf workdir/wex_5.0.0~beta.2/wex
rm workdir/wex_5.0.0~beta.2.orig.tar.gz

mkdir /var/www/build/workdir/wex_5.0.0~beta.2/wex
cd /var/www/build/workdir/wex_5.0.0~beta.2/wex || return
git clone /opt/wex .
rm -rf .git
find . -name ".gitignore" -type f -delete

cd /var/www/build/workdir/ || return
tar -czvf wex_5.0.0~beta.2.orig.tar.gz wex_5.0.0~beta.2/wex

cd /var/www || return
chown -R owner:owner build

# --> pack.sh
