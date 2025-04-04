#!/usr/bin/env bash

docker buildx build -t pax-barcodes -f docker/Dockerfile .
