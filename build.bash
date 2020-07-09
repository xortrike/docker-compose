#!/bin/bash

path=$PWD
name="docker.tar.bz2"

if [ -f "${path}/${name}" ]; then
    rm -f "${path}/${name}"
fi

tar -cvjf "${path}/${name}" \
    --directory="${path}/" ".env" \
    --directory="${path}/" "docker-compose.yml" \
    --directory="${path}/" "apache/apache2.conf" \
    --directory="${path}/" "apache/auth.json" \
    --directory="${path}/" "apache/default.conf" \
    --directory="${path}/" "apache/msmtprc" \
    --directory="${path}/" "apache/php.ini" \
    --directory="${path}/" "apache/php-56-apache" \
    --directory="${path}/" "apache/php-70-apache" \
    --directory="${path}/" "apache/php-71-apache" \
    --directory="${path}/" "apache/php-72-apache" \
    --directory="${path}/" "apache/php-73-apache" \
    --directory="${path}/" "apache/php-74-apache" \
    --directory="${path}/" "mariadb/Dockerfile" \
    --directory="${path}/" "mariadb/mysql.cnf"
