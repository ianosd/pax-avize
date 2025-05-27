#!/usr/bin/env bash
docker run \
    -p 80:80 \
    -v $PWD/misc/server_data:/app/data \
    -e FIREBIRD_DSN="192.168.0.118:/var/lib/firebird/data/CONT_BAZA.FDB" \
    -e FIREBIRD_USER="sysdba" \
    -e FIREBIRD_PASSWORD="mastersaga" \
    ianosd/pax-avize:latest
