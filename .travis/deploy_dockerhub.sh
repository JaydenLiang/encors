#!/bin/bash
docker login -u $DOCKER_USER --password $DOCKER_PASS
if [ "$1" = "staging" ]; then
  TAG="staging"
elif [ "$1" = "production" ]; then
  TAG="latest"
fi

#docker build python
DOCKER_REPO="encors/encors"
docker build -f python/Dockerfile -t $DOCKER_REPO-py:$TAG python/
#docker push $DOCKER_REPO-py
