#!/usr/bin/env bash

odooInit() {
  echo "xmlrpc_port = ${SITE_PORT_RANGE}90" >> ./odoo/config/odoo.conf
}
