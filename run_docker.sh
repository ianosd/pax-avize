#!/usr/bin/env bash
docker run \
    -p 80:80 \
    -v $PWD/misc/server_data:/app/data \
    -e EPAPER_DATA=/app/data ianosd/pax-avize:latest
