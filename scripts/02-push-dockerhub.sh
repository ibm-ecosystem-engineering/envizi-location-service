#!/usr/bin/env bash

echo "build Started ...."

DOCKER_IMAGE=gandigit/e-loc-svc

cd ..

### Linux
podman push $DOCKER_IMAGE-linux:latest

# ### Mac
# podman push $DOCKER_IMAGE-mac:latest

echo "build completed ...."