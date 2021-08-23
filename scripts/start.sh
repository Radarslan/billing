#!/bin/bash

cd patroni &&
docker-compose up -d --build;
cd ..