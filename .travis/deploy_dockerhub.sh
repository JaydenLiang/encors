#!/bin/sh
docker login -u $DOCKER_USER --password $DOCKER_PASS
if [ "$TRAVIS_BRANCH" = "master" ]; then
  TAG="latest"
else
  TAG="$TRAVIS_BRANCH"
fi

#docker build python
DOCKER_REPO="encors/encors"
docker build -f python/Dockerfile -t $DOCKER_REPO-py:$TAG python/
#docker push $DOCKER_REPO-py
