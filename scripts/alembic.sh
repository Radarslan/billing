#!/bin/bash

#docker exec billing alembic downgrade -1
#docker exec billing alembic revision --autogenerate -m "initial"
docker exec billing alembic upgrade head