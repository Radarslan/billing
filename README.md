# Billing

## Requirements
* [Python 3.8](https://www.python.org/downloads/release/python-380/)
* [Poetry](https://python-poetry.org/)
* [Docker](https://www.docker.com/)

### Optional
* [PostgreSQL](https://www.postgresql.org/)

## Description
Service uses docker compose to deploy the application.
This type of deployment was chosen to accommodate requirements 
for High Availability (HA).
PostgreSQL is deployed using [Patroni](https://github.com/zalando/patroni).
It was chosen to imitate fail-safe mechanism to preserve all data.

## Service launch and test
Run following depending on your OS.
For Linux systems use files with "sh" postfix, like ```format.sh```,
for Windows use cmd-files - ```start.cmd```.

###Preferable scripts launch sequence
1. format
2. start
3. alembic (run only on the first launch)
4. test
5. stop

### Scripts

**CAUTION!: check scripts before running them**

* to format
   ```console
   ./scripts/format.sh(.cmd)
   ```
* to start
   ```console
   ./scripts/start.sh(.cmd)
   ```
* to apply alembic revisions
   ```console
   ./scripts/alembic.sh(.cmd)
   ```
* to test
   ```console
   ./scripts/tests.sh(.cmd)
   ```
* to stop
   ```console
   ./scripts/stop.sh(.cmd)
   ```

## Running service URLs

### Documentation
* Swagger <http://127.0.0.1:8000/docs#>
* ReDoc <http://127.0.0.1:8000/redoc#>
