#!/bin/bash

set -e

PLYNX_IMAGES=${PLYNX_IMAGES:="backend ui"}

REPO="n3hub-plynx"
VERSION="0.1";


for IMAGE in ${PLYNX_IMAGES}; do
  docker build --rm -t ${REPO}/${IMAGE}:${VERSION} -f plynx/cdp/docker/${IMAGE}/Dockerfile . ;
  docker tag ${REPO}/${IMAGE}:${VERSION} ${REPO}/${IMAGE}:latest;
done
