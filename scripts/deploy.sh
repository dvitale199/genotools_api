#!/bin/bash

docker build -t us-central1-docker.pkg.dev/genotools/genotools/genotools-api .

# run locally to test endpoint
docker run -d \
    -p 8080:8080 \
    --name genotools-api \
    -v /Users/vitaled2/Desktop/Projects/genotools_api/.secrets/genotools-2f2e43058216.json:/app/genotools-2f2e43058216.json:ro \
    -e GOOGLE_APPLICATION_CREDENTIALS=/app/genotools-2f2e43058216.json \
    us-central1-docker.pkg.dev/genotools/genotools/genotools-api

# test endpoint
python3 genotools_api/test_main.py

# push to artifact registry
docker push us-central1-docker.pkg.dev/genotools/genotools/genotools-api