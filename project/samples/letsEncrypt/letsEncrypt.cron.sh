#!/usr/bin/env bash

certbot-auto --no-self-upgrade certonly

# If the cert updated, we need to update the services using it. E.g.:
if service --status-all | grep -Fq 'apache2'; then
  service apache2 reload
fi
if service --status-all | grep -Fq 'httpd'; then
  service httpd reload
fi
if service --status-all | grep -Fq 'nginx'; then
  service nginx reload
fi

email=$(wex config/getValue -f="/etc/letsencrypt/cli.ini" -k="email" -s=" = ")
domains=$(wex config/getValue -f="/etc/letsencrypt/cli.ini" -k="domains" -s=" = ")
serverIp=$(wex system/ip)

if [ $(wex package/exists -n=mail) == true ]; then
  wexample mailSend -s "Certificate updated on ${serverIp}" ${email} "Your certificate must be up to date for ${domains}"
fi;
