#!/usr/bin/env bash
docker run \
    -p 80:80 \
    -v $PWD/server_data:/app/data \
    -e EPAPER_DATA=/app/data pax-barcodes:latest
