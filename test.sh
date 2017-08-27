#!/bin/bash

docker-compose build
docker-compose run --rm -v `pwd`:/var/app/ webapp python manage.py test