FROM weeger/wexwebserver:latest

# PHP
RUN apt-get install php libapache2-mod-php php-xml -yqq

# Wexample loader for multiple scripts.
RUN w=wexample.sh && curl -sS https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w \
  # Install composer
  && bash $w -s=composerPharInstall -rm \
  # Install Symfony
  && bash $w -s=symfonyClientInstall -rm

COPY ./scripts/docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]
