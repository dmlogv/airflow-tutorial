# Airflow Tutorial

Learning resources for Airflow Tutorial article.


## Contents

- [docker-compose.yml](docker-compose.yml) — An example of Airflow cluster with Celery executor. Contains:
  - Apache Airflow
  - PostgreSQL (Airflow metadata)
  - Redis (Task broker)
  - Celery workers
  - Flower (Celery monitoring)
- [docker-compose.db.yml](docker-compose.db.yml) — Additional database servers and sample data fill up:
  - SQL Server x3 (source database servers)
  - Vertica (target database)
  - `mssql_init` (initialize source data)
- [dags/](dags) — Sample DAGs and common libraries.


## Start and stop

To spin up Airflow cluster only (without databases), use:

```bash
$ docker-compose up --scale worker=3
```

To run all described images and create sample databases, execute:

```bash
$ docker-compose -f docker-compose.yml -f docker-compose.db.yml up --scale worker=3
```

To break down containers press `Ctrl+C` or `Command+C` and the following command:

```bash
$ docker-compose down
```

or

```bash
$ docker-compose -f docker-compose.yml -f docker-compose.db.yml down
```


## Usage

Containers exposes a couple of WebUI's:

- Airflow Webserver: [127.0.0.1:8080](http://127.0.0.1:8080/)
- Flower: [127.0.0.1:5555](http://127.0.0.1:5555/)
