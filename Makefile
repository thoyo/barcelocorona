DOCKER_NAME=barcelocorona
VERSION=0.0.1
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell ip addr show docker0 | grep -Po 'inet \K[\d.]+')

build:
	docker build -t $(DOCKER_NAME_FULL) .

run: build
	docker run -it \
	    --add-host grafana:$(DOCKER_LOCALHOST) \
	    --add-host influxdb:$(DOCKER_LOCALHOST) \
	    --network barcelocorona_private \
	    --name $(DOCKER_NAME) \
	    --rm $(DOCKER_NAME_FULL)

setup:
	docker-compose -f docker-compose.yml up -d
	docker exec -it influxdb bash -c "influx -execute 'create database barcelocorona'"
