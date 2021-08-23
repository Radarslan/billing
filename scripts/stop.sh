#!/bin/bash

cd patroni
docker-compose stop &&
docker-compose rm -f;
cd ..
