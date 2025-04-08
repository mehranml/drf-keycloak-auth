#/bin/bash
docker-compose run --rm api ./manage.py test testapp $@