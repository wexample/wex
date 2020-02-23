#!/usr/bin/env bash

# Init cron
# must be done once cron file is mounted
CRONFILE=/var/default.cron
chown root:root ${CRONFILE}
chmod 0644 ${CRONFILE}
crontab ${CRONFILE}
cron

/bin/bash
