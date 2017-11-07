# Used by this current project to develop locally and make some tests.

FROM wexample/php7:latest

RUN apt-get update

RUN apt-get install \
  # SSH
  openssh-server \
  # Firewall
  ufw -yqq
