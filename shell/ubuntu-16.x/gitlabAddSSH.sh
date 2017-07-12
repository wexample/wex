#!/bin/bash

# Add SSH and prevent host checking.
apt-get install openssh-client -yqq
mkdir -p ~/.ssh
eval $(ssh-agent -s)
[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
