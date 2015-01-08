PROJECT := texastribune
APP := txlege84

IMAGE=${PROJECT}/${APP}
docker/build:
	docker build --tag=${IMAGE} .

prep_for_development:
	python txlege84/manage.py downloadopenstatesdata
	python txlege84/manage.py bulkloadlegislators
	python txlege84/manage.py bulkloadcommittees
	python txlege84/manage.py bulkloadbills -s 83
	python txlege84/manage.py updatebills --bulk
	python txlege84/manage.py bootstraptopics
	python txlege84/manage.py loadfakeissues
	python txlege84/manage.py loadfakeexplainers

PROJECT := texastribune
APP := txlege84

IMAGE=${PROJECT}/${APP}

docker/build:
	docker build --tag=${IMAGE} .

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
