#!/bin/bash

path=$PWD
name="docker.tar.bz2"

if [ -f "${path}/${name}" ]; then
    rm -f "${path}/${name}"
fi

tar -cvjf "${path}/${name}" \
    --directory="${path}/" "README.md" \
    --directory="${path}/" ".env" \
    --directory="${path}/" "docker-compose.yml" \
    --directory="${path}/" "nginx/Dockerfile" \
    --directory="${path}/" "nginx/cert/device.key" \
    --directory="${path}/" "nginx/cert/dhparam.pem" \
    --directory="${path}/" "nginx/openssl/v3.ext" \
    --directory="${path}/" "nginx/openssl/device.key" \
    --directory="${path}/" "nginx/openssl/rootCA.crt" \
    --directory="${path}/" "nginx/openssl/rootCA.key" \
    --directory="${path}/" "nginx/openssl/rootCA.srl" \
    --directory="${path}/" "nginx/openssl/dhparam.pem" \
    --directory="${path}/" "nginx/openssl/create.sh" \
    --directory="${path}/" "nginx/magento.conf" \
    --directory="${path}/" "mariadb/Dockerfile" \
    --directory="${path}/" "mariadb/mysql.cnf" \
    --directory="${path}/" "php/php-5.6-fpm" \
    --directory="${path}/" "php/php-7.0-fpm" \
    --directory="${path}/" "php/php-7.1-fpm" \
    --directory="${path}/" "php/php-7.2-fpm" \
    --directory="${path}/" "php/php-7.3-fpm" \
    --directory="${path}/" "php/php-7.4-fpm" \
    --directory="${path}/" "php/php.ini"
