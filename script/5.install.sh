# 4
# In : docker run -ti ubuntu /bin/bash

# Install Docker repo
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common wget

# For ubuntu
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

echo "deb https://apt.wexample.com/ beta main" >>/etc/apt/sources.list
wget -O - https://apt.wexample.com/gpg | apt-key add -

apt-get update
apt-get install -y wex

####### From gitlab
# https://docs.gitlab.com/ee/user/packages/debian_repository/

#apt-get install -y openssl ca-certificates
#echo -n | openssl s_client -connect gitlab.wexample.com:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' >gitlab.wexample.com.crt
## Debian : cp gitlab.wexample.com.crt /usr/local/share/ca-certificates/
## Ubuntu :
#cp gitlab.wexample.com.crt /etc/ssl/certs/
#update-ca-certificates
#
#CI_API_V4_URL="gitlab.wexample.com/api/v4"
#CI_PROJECT_ID=155
#
##echo "deb [trusted=yes] https://${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/debian/ default beta" | tee /etc/apt/sources.list.d/wex.list
#echo "deb [trusted=yes] https://${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic/ default beta" | tee /etc/apt/sources.list.d/wex.list
#
#deb [trusted=yes] https://gitlab.wexample.com/api/v4/projects/155/packages/debian/ default beta
#                  https://gitlab.wexample.com/api/v4/projects/155/packages/debian/dists/default/beta/binary-amd64/Packages