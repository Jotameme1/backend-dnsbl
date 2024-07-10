#!/bin/bash

print () {
  echo "$1[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $2"
}

print "[INFO]" "Comprobando variables de entorno"

## Variables de entorno
print "[INFO]" "ENVIRONMENT             : ${ENVIRONMENT}"
print "[INFO]" "MYSQL_HOST              : ${MYSQL_HOST}"
print "[INFO]" "MYSQL_PORT              : ${MYSQL_PORT}"
print "[INFO]" "SDC_USER                : ${SDC_USER}"
print "[INFO]" "SDC_PASSWORD            : ${SDC_PASSWORD}"
print "[INFO]" "SDC_DATABASE            : ${SDC_DATABASE}"
print "[INFO]" "BALANCER_USER           : ${BALANCER_USER}"
print "[INFO]" "BALANCER_PASSWORD       : ${BALANCER_PASSWORD}"
print "[INFO]" "BALANCER_DATABASE       : ${BALANCER_DATABASE}" 
print "[INFO]" "APP_NAME                : ${APP_NAME}"
print "[INFO]" "INSTALL_NEWRELIC        : ${INSTALL_NEWRELIC}"

print "[INFO]" "Generando Variables de Entorno"
printenv | sed 's/^\(.*\)$/export \1/g' > /env.sh
sed -Ei "s/(.*)=(.*)/\1=\'\2\'/g" /env.sh
chmod +x /env.sh

cat > /opt/back_dnsrbl/database/__init__.py <<EOF
""" database contiene las funciones para interactuar con las bases de datos """
import os

#SDC DATABASE
sdc_host = "${MYSQL_HOST}"
sdc_port = ${MYSQL_PORT}
sdc_user = "${SDC_USER}"
sdc_password = "${SDC_PASSWORD}"
sdc_database = "${SDC_DATABASE}"

#DISK BALANCER DATABASE
balancer_host = "${MYSQL_HOST}"
balancer_port = ${MYSQL_PORT}
balancer_user = "${BALANCER_USER}"
balancer_password = "${BALANCER_PASSWORD}"
balancer_database = "${BALANCER_DATABASE}"
EOF

cat > /opt/back_dnsrbl/__init__.py <<EOF
import os
environment = "${ENVIRONMENT}"
EOF

if [[ "$ENVIRONMENT" == "production" ]]; then
sed -i 's/#//g' /var/spool/cron/crontabs/root
fi


#Apply crontabs
/usr/bin/crontab /var/spool/cron/crontabs/root

# Start supervisord and services
/usr/bin/supervisord -n -c /etc/supervisord.conf
