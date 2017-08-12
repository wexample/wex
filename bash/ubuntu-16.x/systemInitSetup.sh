#!/usr/bin/env bash

# Inspired by DigitalOcean tutorial.
systemInitSetup() {

  # Install wexample if not already done.
  if [[ -f /opt/wexample ]]; then
    w=_install.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w && bash $w && rm -rf $w
  fi;

  # Manage arguments
  for i in "$@"
  do
    case $i in
        -u=*|--user=*)
        user="${i#*=}"
        shift # past argument
        ;;
        -p=*|--password=*)
        password="${i#*=}"
        shift # past argument
        ;;
    esac
  done

  systemIp=$(wexample systemGetIp)

  # Create a new super user.
  useradd -g sudo -ms /bin/bash -p $(echo ${password} | openssl passwd -1 -stdin) ${user}

  # Create SSH dir.
  mkdir /home/${user}/.ssh
  chown ${user}:sudo /home/${user}/.ssh
  chmod 700 /home/${user}/.ssh

  # Add wexample SSH key
  wexample fileTextAppend /home/${user}/.ssh/authorized_keys $(< ${WEX_DIR_ROOT}ssh/id_rsa.pub)
  chown ${user}:sudo /home/${user}/.ssh/authorized_keys
  chmod 600 /home/${user}/.ssh/authorized_keys

  # Set a custom port for SSH
  wexample configChangeValue /etc/ssh/sshd_config Port 2299

  service ssh restart

  # Disable password authentication
  configFile=/etc/ssh/ssh_config
  wexample configUncomment ${configFile} 'PasswordAuthentication'
  wexample configChangeValue ${configFile} 'PasswordAuthentication' 'no'

  # May display an error when running from Docker
  # https://stackoverflow.com/questions/39169403/systemd-and-systemctl-within-ubuntu-docker-images
  systemctl reload sshd

  # Firewall
  # Install if not exists
  apt-get install ufw -yqq

  # Disallow IPV6 to prevent firewall warnings
  wexample configSetValue /etc/default/ufw "IPV6" "no" "="
  # Allow SSH
  ufw allow OpenSSH
  ufw enable

  # Enable HTTPS
  a2enmod ssl
  service apache2 restart

  # Create a Self-Signed SSL Certificate
  mkdir /etc/apache2/ssl

  wexample httpsInstall

  # TODO HTTPS (certificates)
  # TODO Séparer les fonctions : SSH seuleulement pour un serveur hôte. Apache aussi ? / HTTPS pour un container... Qu'on peut préparer dans un dockerfile ?
}
