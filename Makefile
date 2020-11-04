.PHONY: test # @see https://stackoverflow.com/a/3931814
TARGET = postgres:alpine
CONTAINER = $$(docker ps | grep $(TARGET) | xargs -n1 2>/dev/null | head -n1)
ENV_FILE = $(shell pwd)/.env
FLASK_ENV = $$(. $(ENV_FILE); printf "%s" "$${FLASK_ENV}")
#HOST = $$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(CONTAINER))
INSPECT = $$(docker image inspect $(TARGET) 2>/dev/null | sed ':a;N;$!ba;s/\n//g')
NETWORK = $$(docker-machine ip default)
PIP_PREPARE = pip install --user python-dotenv pythonloc
PIP_REQUIRE = piploc install -r requirements/prod.txt
PIP_REQ_DEV = piploc install -r requirements/dev.txt
PIP_RUN = pipx run --pypackages
PORT = $$(docker inspect -f '{{.Config.ExposedPorts}}' $(TARGET) | sed 's/map\[\([0-9]*\)\/.*/\1/')
#SHELL := /usr/bin/env bash # @see https://stackoverflow.com/a/43566158
STAMP = $$(printf "%s_%s" "$$(printf "%s" "$(TARGET)" | cut -d: -f1)" "$$(date +"%Y-%m-%d_%H-%M-%S")")

clean:
	test "$(FLASK_ENV)" == "development" && $(PIP_RUN) flask clean || printf "%s" "ERROR: Cleaner requires development environment."

clean-adminer: stop-adminer
	# @see https://success.docker.com/article/how-to-remove-a-signed-image-with-a-none-tag
	#docker images --digests adminer
	docker rmi --force adminer

clean-all: stop-all clean
	yes | docker system prune -a

clean-all-volumes: stop-all clean
	yes | docker system prune -a --volumes

clean-target: stop-target
	test "$(INSPECT)" == "[]" || docker rmi $(TARGET)

designer:
	test "$(FLASK_ENV)" == "development" && $(PIP_RUN) designer || printf "%s" "ERROR: Designer requires development environment."

env:
	printf "%s" "$(FLASK_ENV)"

freeze:
	# @see https://medium.com/@grassfedcode/goodbye-virtual-environments-b9f8115bc2b6
	pipfreezeloc | tr 'A-Z' 'a-z' | sort

help:
	$(PIP_RUN) flask --help

help-db:
	$(PIP_RUN) flask db --help

help-ps:
	$(PIP_RUN) flask ps --help

install:
	$(PIP_PREPARE)
	yarn --cwd assets install
	test "$(FLASK_ENV)" == "development" && $(PIP_REQ_DEV) | tee || $(PIP_REQUIRE) | tee

lint:
	test "$(FLASK_ENV)" == "development" && ($(PIP_RUN) flask lint --fix-imports || exit 0) || printf "%s" "ERROR: Linter requires development environment."

list:
	docker ps --size

log-adminer:
	docker-compose logs | grep adminer || exit 0

log-target:
	test -z "$(CONTAINER)" || docker logs $(CONTAINER)

network:
	printf "%s" "$(NETWORK)"

parcel-build:
	yarn --cwd assets run build

parcel-start:
	yarn --cwd assets run start

port: start-target
	printf "%s" "$(PORT)"

routes:
	$(PIP_RUN) flask routes

run:
	$(PIP_RUN) flask run --with-threads

shell:
	$(PIP_RUN) flask shell

start: start-target parcel-build run

start-adminer:
	docker-compose up --detach --remove-orphans adminer && printf "adminer is running at http://%s:%s" "$(NETWORK)" "$$(docker inspect -f '{{.Config.ExposedPorts}}' adminer | sed 's/map\[\([0-9]*\)\/.*/\1/')"

start-target:
	test -z "$(CONTAINER)" && docker pull $(TARGET) || exit 0
	#TODO: add --volume
	test -z "$(CONTAINER)" && docker run --detach --env-file $(ENV_FILE) --hostname $(STAMP) --name $(STAMP) --publish $(PORT):$(PORT) --rm $(TARGET) || exit 0
	printf "%s is running at http://%s:%s" "$(TARGET)" "$(NETWORK)" "$(PORT)"

start-ui: start-target parcel-build ui

stop-adminer:
	docker-compose stop adminer

stop-all:
	#TODO: shutdown werkzeug
	docker stop $$(docker ps -q) || exit 0

stop-target:
	test -z "$(CONTAINER)" || docker stop $(CONTAINER)

test:
	python test/app_test.py

ui:
	python src/app.py

update:
	#pip install --upgrade pip
	$(PIP_PREPARE) --upgrade
	yarn --cwd assets upgrade
	test "$(FLASK_ENV)" == "development" && $(PIP_REQ_DEV) --upgrade | tee || $(PIP_REQUIRE) --upgrade | tee
