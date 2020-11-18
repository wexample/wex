#!/usr/bin/env bash

certGenerateArgs() {
  _DESCRIPTION="Generates a self signed certificate for a local use to allow testing Progressive Web Applications."
  _ARGUMENTS=(
    [0]='self_signed s "Self signed. Beware ! The unsigned version is not bug-free at the moment." false'
    [1]='passphrase p "The password that we will pass to openssl." false'
    [2]='common_name c "Common name" false'
    [3]='state_or_province_name st "State or province name" false'
    [4]='country_name ct "Country name (2 letter code)" false'
    [5]='email_address e "Email address" false'
    [6]='organization_name o "Organization name" false'
    [7]='organizational_unit_name ou "Organizational Unit Name" false'
  )
}

erasePreviousLines()
{
    # \033[<N>A move the cursor up N lines
    # \033[K erase to end of line

    for ((i=1; i<$1 + 1; ++i))
    do
        echo -en "\033[1A\033[K"
    done
}

certGenerate() {
  # TODO Common name for caconfig.cnf should be a domain name that can be retrieved automatically
  # TODO Fix behaviour when do not want to sign the certificate
  # TODO Create a slug based on the project folder name for the COMMON_NAME default value

  # DEFINING VARIABLES
  ####################

  # We must be into the certificate folder

  # Ensures that we a passphrase
  local PASSPHRASE=${PASSPHRASE:-password}

  # project folder
  local PROJECT_FOLDER_NAME="$(basename $(pwd))"

  # main certificates folder
  local CERT_FOLDER='./tmp/certs/';

  # will contain the private key
  local PRIVATE_FOLDER=${CERT_FOLDER}'private/';

  # will contain the certificate configuration files
  local CONFIG_FOLDER=${CERT_FOLDER}'conf/'

  if [[ ${SELF_SIGNED} == true ]]; then
    # will contain the signed certificates
    local SIGNED_CERTS=${CERT_FOLDER}'signedCerts/'

    # will contain your certificate authority configuration file
    local CA_CONFIG=${CONFIG_FOLDER}'caconfig.cnf'

    local INDEX_ATTR=${CERT_FOLDER}'index.txt.attr'
    local SERIAL=${CERT_FOLDER}'serial'
    local INDEX=${CERT_FOLDER}'index.txt'
    local CACERT_PEM=${CERT_FOLDER}'cacert.pem'
    local CAKEY_PEM=${PRIVATE_FOLDER}'cakey.pem'
  fi

  # will contain the informations that allows to generate the self signed certificate
  local LOCALHOST_CONFIG=${CONFIG_FOLDER}'localhost.cnf'

  local TEMP_KEY=${CERT_FOLDER}'tempkey.pem'
  local TEMP_REQ=${CERT_FOLDER}'tempreq.pem'
  local SERVER_KEY=${CERT_FOLDER}'server_key.pem'
  local SERVER_CRT=${CERT_FOLDER}'server_crt.pem'

  # 1. Creating architecture
  ##########################

  echo -ne $(wex text/color -c=lightblue -t='Generating folders if needed...')
  mkdir -p ${PRIVATE_FOLDER}

  if [[ ${SELF_SIGNED} == true ]]; then
    mkdir -p ${SIGNED_CERTS}
  fi

  mkdir -p ${CONFIG_FOLDER}

  if [[ ${SELF_SIGNED} == true ]]; then
    echo -ne "\r"$(wex text/color -c=lightblue -t='Folders ')
    echo -n $(wex text/color -c=lightcyan -t="${PRIVATE_FOLDER}")
    echo -n ' '$(wex text/color -c=lightblue -t='and ')
    echo -n ' '$(wex text/color -c=lightcyan -t="${SIGNED_CERTS}")
    echo ' '$(wex text/color -c=lightblue -t='created (if they did not already exist).')
  else
    echo -ne "\r"$(wex text/color -c=lightblue -t='Folder ')
    echo -n $(wex text/color -c=lightcyan -t="${PRIVATE_FOLDER}")
    echo ' '$(wex text/color -c=lightblue -t='created (if it did not already exist).')
  fi

  # 2. Certificate database creation
  ##################################
  if [[ ${SELF_SIGNED} == true ]]; then
    if [[ ! -f ${SERIAL} ]] || [[ ! -f ${INDEX} ]] ; then
        echo -ne $(wex text/color -c=lightblue -t='Certificate database creation...')

        if [[ ! -f ${SERIAL} ]]; then
            echo '01' > ${SERIAL}
        fi

        if [[ ! -f ${INDEX} ]]; then
            touch ${INDEX}
        fi

        echo -ne "\r"$(wex text/color -c=lightblue -t='Certificate database created in ')
        echo -n ' '$(wex text/color -c=lightcyan -t="${SERIAL}")
        echo -n $(wex text/color -c=lightblue -t=' and')
        echo -ne ' '$(wex text/color -c=lightcyan -t="${INDEX}")
        wex text/color -c=lightblue -t='.'
    fi
  fi

  # 3. Certificate authority configuration file creation. /!\ This file will have to be edited !
  ##############################################################################################

  if [[ ! -f ${CA_CONFIG} && ! -f ${LOCALHOST_CONFIG} ]]; then
    local COMMON_NAME=${COMMON_NAME:-${PROJECT_FOLDER_NAME}.wex}
    local STATE_OR_PROVINCE_NAME=${STATE_OR_PROVINCE_NAME:-'WEX LAND'}
    local COUNTRY_NAME=${COUNTRY_NAME:-'WX'}
    local EMAIL_ADDRESS=${EMAIL_ADDRESS:-contact@${PROJECT_FOLDER_NAME}.wex}
    local ORGANIZATION_NAME=${ORGANIZATION_NAME:-'WEX ORGANIZATION'}
    local ORGANIZATIONAL_UNIT_NAME=${ORGANIZATION_UNIT_NAME:-'WEX IT'}
  fi

  if [[ ! -f ${CA_CONFIG} ]]; then
    echo -n $(wex text/color -c=lightblue -t='Generating the certificate authority configuration file in ')
    echo ' '$(wex text/color -c=lightcyan -t="${CA_CONFIG}").

    echo -e "[ ca ]\n\
default_ca = local_ca\n\
\n\
[ local_ca ]\n\
dir = ${CERT_FOLDER}\n\
certificate = ${CACERT_PEM}\n\
database = ${INDEX}\n\
new_certs_dir = ${SIGNED_CERTS}\n\
private_key = ${CAKEY_PEM}\n\
serial = ${SERIAL}\n\
\n\
default_crl_days = 365\n\
default_days = 1825\n\
default_md = sha256\n\
\n\
policy = local_ca_policy\n\
x509_extensions = local_ca_extensions\n\
\n\
copy_extensions = copy\n\
\n\
[ local_ca_policy ]\n\
commonName = supplied\n\
stateOrProvinceName = supplied\n\
countryName = supplied\n\
emailAddress = supplied\n\
organizationName = supplied\n\
organizationalUnitName = supplied\n\
\n\
[ local_ca_extensions ]\n\
basicConstraints = CA:false\n\
\n\
[ req ]\n\
default_bits = 2048\n\
default_keyfile = ${CAKEY_PEM}\n\
default_md = sha256\n\
\n\
prompt = no\n\
distinguished_name = root_ca_distinguished_name\n\
x509_extensions = root_ca_extensions\n\
\n\
[ root_ca_distinguished_name ]\n\
commonName = ${COMMON_NAME}\n\
stateOrProvinceName = ${STATE_OR_PROVINCE_NAME}\n\
countryName = ${COUNTRY_NAME}\n\
emailAddress = ${EMAIL_ADDRESS}\n\
organizationName = ${ORGANIZATION_NAME}\n\
organizationalUnitName = ${ORGANIZATIONAL_UNIT_NAME}\n\
\n\
[ root_ca_extensions ]\n\
basicConstraints = CA:true\n" > ${CA_CONFIG}

    erasePreviousLines 1

    echo -n $(wex text/color -c=lightblue -t='Certificate authority configuration file ')
    echo -n ' '$(wex text/color -c=lightcyan -t="${CA_CONFIG}")
    wex text/color -c=lightblue -t=' created and configured.'
  fi

  # To ensure us that openssl take our values into account
  export OPENSSL_CONF=${CA_CONFIG}

  # 4. Certification authority generation
  #######################################
  wex text/color -c=lightblue -t='Generating the certification authority...'
  openssl req -x509 -newkey rsa:2048 -out ${CACERT_PEM} -outform PEM -days 1825 -passout pass:"${PASSPHRASE}"

  echo -ne $(wex text/color -c=lightcyan -t="${CACERT_PEM}")
  echo -n $(wex text/color -c=lightblue -t=' and')
  echo -ne ' '$(wex text/color -c=lightcyan -t="${CAKEY_PEM}")
  wex text/color -c=lightblue -t=' files are generated.'

  if [[ ! -f ${LOCALHOST_CONFIG} ]]; then
    echo -e "[ req ]\n\
prompt = no\n\
distinguished_name = server_distinguished_name\n\
req_extensions = v3_req\n\
\n\
[ server_distinguished_name ]\n\
commonName = WexampleLabsCA\n\
stateOrProvinceName = ${STATE_OR_PROVINCE_NAME}\n\
countryName = ${COUNTRY_NAME}\n\
emailAddress = ${EMAIL_ADDRESS}\n\
organizationName = ${ORGANIZATION_NAME}\n\
organizationalUnitName = ${ORGANIZATIONAL_UNIT_NAME}\n\
\n\
[ v3_req ]\n\
basicConstraints = CA:FALSE\n\
keyUsage = nonRepudiation, digitalSignature, keyEncipherment\n\
subjectAltName = @alt_names\n\
\n\
[ alt_names ]\n\
DNS.0 = localhost\n\
DNS.1 = ${COMMON_NAME}\n" > ${LOCALHOST_CONFIG}

    echo -n $(wex text/color -c=lightblue -t='Generating the certificate authority configuration file in ')
    wex text/color -c=lightcyan -t="${LOCALHOST_CONFIG}".

    erasePreviousLines 1

    echo -n $(wex text/color -c=lightblue -t='Certificate authority configuration file ')
    echo -n ' '$(wex text/color -c=lightcyan -t="${LOCALHOST_CONFIG}")
    wex text/color -c=lightblue -t=' created and configured.'
  fi

  # To ensure us that openssl take our values into account
  export OPENSSL_CONF=${LOCALHOST_CONFIG}

  # 5. Final certificate and key generation CHECK
  #########################################

  wex text/color -c=lightblue -t='Generating the certificate and the key... (Same password as before)'
  openssl req -newkey rsa:2048 -keyout ${TEMP_KEY} -keyform PEM -out ${TEMP_REQ} -outform PEM -passout pass:"${PASSPHRASE}"

  echo -ne $(wex text/color -c=lightcyan -t="${TEMP_KEY}")
  echo -ne $(wex text/color -c=lightblue -t=' and the certificate')
  echo -ne $(wex text/color -c=lightcyan -t=" ${TEMP_REQ}")
  wex text/color -c=lightblue -t=' have been generated.'

  echo -ne $(wex text/color -c=lightblue -t='Generating ')
  wex text/color -c=lightcyan -t="${SERVER_KEY}" ...

  openssl rsa -passin pass:"${PASSPHRASE}" < ${TEMP_KEY} > ${SERVER_KEY}

  # Erase previous useless text
  erasePreviousLines 3

  echo -ne $(wex text/color -c=lightblue -t='The RSA key')
  echo -ne $(wex text/color -c=lightcyan -t=" ${SERVER_KEY}")
  wex text/color -c=lightblue -t=' has been generated.'

  # 6. Attribute file generation
  ##############################
  echo -ne $(wex text/color -c=lightblue -t='Regenerating serial file')
  echo -ne $(wex text/color -c=lightblue -t=" ${SERIAL}")
  wex text/color -c=lightblue -t=' ...'

  echo '01' > ${SERIAL}

  erasePreviousLines 1

  wex text/color -c=lightblue -t='Serial file ${SERIAL}...'

  if [[ ! -f ${INDEX_ATTR} ]]; then
      echo -ne $(wex text/color -c=lightblue -t='Generating an attribute file ...')

      echo 'unique_subject = yes/no' > ${INDEX_ATTR}

      erasePreviousLines 1

      echo -ne "\r"$(wex text/color -c=lightblue -t='Attribute file')
      echo -ne $(wex text/color -c=lightcyan -t=" ${INDEX_ATTR}")
      wex text/color -c=lightblue -t=' created.'
  fi

  # 7. Signing the certificate
  ############################

  if [[ ${SELF_SIGNED} != true ]]; then
    wex text/color -c=lightblue -t='Done !'
    exit 0;
  fi

  # We switch back to the first configuration file to ensure us that openssl take our values into account
  export OPENSSL_CONF=${CA_CONFIG}

  # The batch option is here to automatically confirm the signature, avoiding interaction with the user
  openssl ca -in ${TEMP_REQ} -out ${SERVER_CRT} -passin pass:${PASSPHRASE} -batch

  wex text/color -c=lightblue -t='Done !'
  exit 0;
}