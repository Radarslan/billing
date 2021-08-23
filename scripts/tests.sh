#!/bin/bash

docker exec billing mypy /app
docker exec billing pytest /app/tests