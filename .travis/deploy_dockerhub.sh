#!/bin/bash
docker login -u $DOCKER_USER --password $DOCKER_PASS
if [ "$1" = "develop" ]; then
    TAG="develop"
elif [ "$1" = "staging" ]; then
    TAG="staging"
elif [ "$1" = "production" ]; then
    TAG="latest"
else
    TAG="test"
fi

#docker build python
DOCKER_REPO="encors/encors-py"
docker build -f python/Dockerfile -t $DOCKER_REPO:$TAG python/
#push to docker hub
if [ "$2" = "push" ]; then
    docker push $DOCKER_REPO
fi
