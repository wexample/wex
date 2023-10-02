#!/usr/bin/env bash

gpg --armor --export contact@wexample.com > .wex/source/gpg/public.key
gpg --export-secret-keys -a contact@wexample.com > .wex/source/gpg/private.key.asc

# In container
#gpg --import /root/.gnupg/private.key.asc
#gpg --import /root/.gnupg/public.key
