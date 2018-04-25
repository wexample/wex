#!/usr/bin/env bash

letsEncryptInstall() {
  SITE_DOMAIN=${1}
  EMAIL=${2}
  SITE_DIR_ROOT=${3}

  # Create dir if not exists.
  mkdir -p ${SITE_DIR_ROOT}

  # Install cert bot
  wget https://dl.eff.org/certbot-auto
  chmod a+x certbot-auto
  mv certbot-auto /usr/local/bin

  # Install the dependencies.
  certbot-auto --noninteractive --os-packages-only

  # Set up config file.
  mkdir -p /etc/letsencrypt

  # Set configuration
  CONF=/etc/letsencrypt/cli.ini
  cp ${WEX_DIR_SAMPLES}"letsEncrypt/letsEncrypt.cli.ini" ${CONF}

  wexample configChangeValue ${CONF} "email" "${EMAIL}" " = "
  wexample configChangeValue ${CONF} "domains" "${SITE_DOMAIN}, www.${SITE_DOMAIN}" " = "
  wexample configChangeValue ${CONF} "webroot-path" "${SITE_DIR_ROOT}" " = "

  # Install cron
  CRON_SCRIPT=/etc/cron.daily/certbot-renew
  cp ${WEX_DIR_ROOT}"letsEncrypt/letsEncrypt.cron.sh" ${CRON_SCRIPT}

  # Execute cron once (should send confirmation mail)
  . ${CRON_SCRIPT}
}
