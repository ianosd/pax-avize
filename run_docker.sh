#!/usr/bin/env bash
docker run \
    -p 80:80 \
    -v $PWD/app_data:/app/data \
    -e EPAPER_DATA=/app/data ianosd/pax-avize:latest
