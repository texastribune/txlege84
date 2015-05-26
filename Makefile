PROJECT := texastribune
APP := txlege84
IMAGE=${PROJECT}/${APP}
FOO ?= 83

# can override with an environment variable:
DOCKER_DATABASE_URL?=postgresql://docker:docker@db:5432/docker
S3_SOURCE?=s3://${APP}-postgres-exports/pg.dump

new_prep_for_development:
	python txlege84/manage.py bootstrapchamber
	python txlege84/manage.py bootstrapparty
	python txlege84/manage.py bootstrapsubject
	python txlege84/manage.py bootstraplegislator

prep_for_development:
	python txlege84/manage.py downloadopenstatesdata
	python txlege84/manage.py bulkloadlegislators
	python txlege84/manage.py bulkloadcommittees
	python txlege84/manage.py bulkloadbills -s $(FOO)
	python txlege84/manage.py bootstraptopics
	python txlege84/manage.py loadfakeissues
	python txlege84/manage.py loadfakeexplainers


local/datadump:
	aws s3 cp --profile newsapps ${S3_SOURCE} pg.dump

local/loaddata: local/datadump
	dropdb txlege84
	createdb txlege84
	pg_restore -d txlege84 pg.dump

pull:
	git pull

master:
	git checkout master

staging:
	git checkout staging

docker/build:
	docker build --tag=${IMAGE} .

docker/prod: pull master docker/build
	-docker stop ${APP} && docker rm ${APP}
	docker run --name=${APP} \
		--hostname=${APP}-prod \
		--detach=true \
		--publish=80:8000 \
		--env-file=env ${IMAGE}

docker/staging: pull staging docker/build
	-docker stop ${APP} && docker rm ${APP}
	docker run --name=${APP} \
		--hostname=${APP}-staging \
		--detach=true \
		--publish=80:8000 \
		--env-file=env ${IMAGE}

docker/util: docker/build
	cd util; make; cd ..
	docker run --env-file=env \
		-it --rm ${APP}-util bash

docker/debug: docker/build
	docker run --rm -it --volumes-from=${APP} --entrypoint=/bin/bash --workdir=/app/logs ${IMAGE}

### for development only from here on:

docker/db-data:
	# NOTE: this will issue an error if the container is already there; it can be safely ignored
	# I'd like a better way to be idempotent
	-docker create \
		--name ${APP}-db-data \
		texastribune/postgres

# start the db if it's there; if not create it
docker/db: docker/db-data
	docker start ${APP}-dev-db || docker run --detach \
		--volumes-from=${APP}-db-data \
		--publish=5432:5432 \
		--name=${APP}-dev-db \
		texastribune/postgres

# pull from an export on S3 to populate the db:
docker/refresh-db:
	docker run -it --rm \
		--link=${APP}-dev-db:db \
		--env=AWS_ACCESS_KEY_ID \
		--env=AWS_SECRET_ACCESS_KEY \
		--env=DATABASE_URL=${DOCKER_DATABASE_URL} \
		--env=S3_SOURCE=${S3_SOURCE} \
		texastribune/pg-tools /app/import-from-s3.sh

# reset the DB to what the production one looks
# like without pulling a new copy from S3
docker/reset-db:
	docker run -it --rm \
		--link=${APP}-dev-db:db \
		--env=DATABASE_URL=${DOCKER_DATABASE_URL} \
		--entrypoint=phd \
		texastribune/pg-tools "dropdb" "--if-exists"
	docker run -it --rm \
		--link=${APP}-dev-db:db \
		--env=DATABASE_URL=${DOCKER_DATABASE_URL} \
		--entrypoint=phd \
		texastribune/pg-tools "createdb" "--template=template_db"

docker/clean:
	-docker stop ${APP}-dev-db
	-docker rm ${APP}-dev-db

docker/run: docker/build docker/db
	docker run --entrypoint=bash \
		-it \
		--rm \
		--publish=8000:8000 \
		--env-file=env \
		--link=${APP}-dev-db:db \
		--name=${APP}-dev ${IMAGE}
