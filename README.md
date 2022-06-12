# SimpleCMS

## How to run

```bash
docker-compose up

# upgrade db to latest version
docker-compose exec web aerich upgrade
```

## Run tests
```bash
docker-compose exec web python -m pytest -s
```

## How to make migrations

```bash
docker-compose exec web aerich migrate --name my_migration_name
```
