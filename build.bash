#!/bin/bash

path=$PWD
name="docker.tar.bz2"

if [ -f "${path}/${name}" ]; then
    rm -f "${path}/${name}"
fi

tar -cvjf "${path}/${name}" \
    --directory="${path}/" ".env" \
    --directory="${path}/" "docker-compose.yml" \
    --directory="${path}/" "mariadb/" \
    --directory="${path}/" "apache/"
