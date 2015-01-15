PROJECT := texastribune
APP := txlege84
IMAGE=${PROJECT}/${APP}
FOO ?= 83

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

pull:
	git pull

docker/build:
	docker build --tag=${IMAGE} .

docker/prod: pull docker/build
	-docker stop ${APP} && docker rm ${APP}
	docker run --name=${APP} \
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

docker/db:
	docker start ${APP}-dev-db || docker run --detach \
		--publish=5432:5432 \
		--name=${APP}-dev-db \
		texastribune/postgres

docker/clean:
	-docker stop ${APP}-dev-db
	-docker rm ${APP}-dev-db

docker/run: docker/build docker/db
	docker run --entrypoint=bash \
		-it \
		--rm \
		--publish=8000:8000 \
		--env-file=.env \
		--link=${APP}-dev-db:db \
		--name=${APP}-dev ${IMAGE}
