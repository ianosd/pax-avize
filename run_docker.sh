#!/usr/bin/env bash
docker run \
    -p 80:80 \
    -v $PWD/app_data:/app/data \
    -e FIREBIRD_DSN="localhost:/var/lib/firebird/data/CONT_BAZA.FDB" \
    -e FIREBIRD_USER="sysdba" \
    -e FIREBIRD_PASSWORD="password" \
    ianosd/pax-avize:latest
