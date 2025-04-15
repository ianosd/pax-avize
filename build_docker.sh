#!/usr/bin/env bash
cd frontend
npm run build
cd ..

docker buildx build -t ianosd/pax-avize -f docker/Dockerfile .
