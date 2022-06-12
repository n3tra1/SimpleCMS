# SimpleCMS

## How to run

```bash
docker-compose up

# upgrade db to latest version
docker-compose exec web aerich upgrade
```

# Docs 
http://0.0.0.0:8000/swagger/  
http://0.0.0.0:8000/redoc/

## Run tests
```bash
docker-compose exec web python -m pytest
# run coverage
docker-compose exec web coverage run -m pytest
# coverage report
docker-compose exec web coverage report -m
```

## How to make migrations

```bash
docker-compose exec web aerich migrate --name my_migration_name
```
## ENVIRONMENT VARIABLES
```bash
ENVIRONMENT (default="dev") - name of environment
DATABASE_URL - standard database URI (e.g. postgres://postgres:postgres@web-db:5432/web_dev)
DATABASE_URL - standard database URI for tests (e.g. postgres://postgres:postgres@web-db:5432/web_dev)
ARTICLE_PAGINATION_LIMIT (default=500) - maximal limit for GET /article method
JWT_SECURITY_KEY - your secret for JWT signing
JWT_TTL_SECONDS - time to live for JWT token in seconds
SWAGGER_PATH - path to swagger docs
REDOC_PATH - path to redoc docs
OPENAPI_PATH - path to openapi.json
```