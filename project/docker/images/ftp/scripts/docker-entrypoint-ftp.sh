#!/usr/bin/env bash

/run.sh -c 30 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P ${PUBLICHOST} -p ${PORTS_RANGE}

/bin/bash

