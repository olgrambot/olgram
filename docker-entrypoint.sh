#!/bin/bash
set -e

if [ ! -z "${CUSTOM_CERT}" ]; then
  echo "Use custom certificate"
  if [ ! -f /cert/private.key ]; then
    echo "Generate new certificate"
    openssl req -newkey rsa:2048 -sha256 -nodes -keyout /cert/private.key -x509 -days 10000 -out /cert/public.pem -subj "/C=US/ST=Berlin/L=Berlin/O=my_org/CN=${WEBHOOK_HOST}"
  fi
fi

sleep 10
aerich upgrade
python migrate.py
python main.py $@
