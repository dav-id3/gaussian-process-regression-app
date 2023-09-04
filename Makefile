#!make

cmd=current

PROJECT_NAME := gaussian-process-regression-app
DOCKER_NETWORK := $(PROJECT_NAME)-network

#port
MYSQL_PORT := 3306
API_PORT := 8000
WEB_PORT := 3000

#containers name
DATABASE_CONTAINER := $(PROJECT_NAME)-db
MIGRATION_CONTAINER := $(PROJECT_NAME)-migraiton
API_CONTAINER := $(PROJECT_NAME)-api
OPENAPI_CONTAINER := $(PROJECT_NAME)-openapi
WEB_CONTAINER := $(PROJECT_NAME)-web

#path
DATABASE_FOLDER := $(CURDIR)/db
MIGRATION_FOLDER := $(CURDIR)/migration
API_FOLDER := $(CURDIR)/api
OPENAPI_FOLDER := $(CURDIR)/openapi
WEB_FOLDER := $(CURDIR)/web
ENVFILE_FOLDER := $(CURDIR)/envfiles
OPENAPI_COMPILED_FILE := $(OPENAPI_FOLDER)/compiled.yaml

##Network
.PHONY: network.create
network.create:
	@docker network create --driver bridge $(DOCKER_NETWORK)

.PHONY: network.remove
network.remove:
	@docker network rm $(DOCKER_NETWORK)

##Database
.PHONY: db.build
db.build:
	@docker build \
		-f $(DATABASE_FOLDER)/Dockerfile \
		-t $(DATABASE_CONTAINER) $(DATABASE_FOLDER) 

.PHONY: db.start
db.start:
	@docker run -d --rm \
		--env-file $(ENVFILE_FOLDER)/.db \
		--net $(DOCKER_NETWORK) \
		--name $(DATABASE_CONTAINER) \
		--volume $(DATABASE_FOLDER)/data:/var/lib/mysql:rw \
		--publish $(MYSQL_PORT):3306 \
		$(DATABASE_CONTAINER)

.PHONY: db.exec
db.exec:
	@docker exec -it $(DATABASE_CONTAINER) /bin/bash

## Migration for database
.PHONY: migration.build
migration.build:
	@docker build \
		-f $(MIGRATION_FOLDER)/Dockerfile \
		-t $(MIGRATION_CONTAINER) ${MIGRATION_FOLDER}

.PHONY: migration.run
migration.run:
	@docker run --rm -it \
		--env-file $(ENVFILE_FOLDER)/.alembic \
		--net $(DOCKER_NETWORK) \
		--name $(MIGRATION_CONTAINER) \
		--volume ${MIGRATION_FOLDER}/alembic:/workspace/alembic:rw \
		$(MIGRATION_CONTAINER) alembic ${cmd}

.PHONY: migration.test
migration.test:
	@docker run --rm \
		--volume ${MIGRATION_FOLDER}/alembic:/workspace/alembic:ro
		$(MIGRATION_CONTAINER) isort alembic --check-only --diff
	@docker run --rm 
		--volume ${MIGRATION_FOLDER}/alembic:/workspace/alembic:ro
		$(MIGRATION_CONTAINER) black alembic --check --diff
		
## api
.PHONY: api.build
api.build:
	@docker build \
		-f $(API_FOLDER)/Dockerfile \
		-t $(API_CONTAINER) ./api

.PHONY: api.up
api.up:
	@docker run --rm -it \
		--env-file $(ENVFILE_FOLDER)/.api \
		--net $(DOCKER_NETWORK) \
		--name $(API_CONTAINER) \
		--publish ${API_PORT}:8000 \
		$(API_CONTAINER)

.PHONY: api.test
api.test:
	@docker run --rm ${API_CONTAINER} isort src --check-only --diff
	@docker run --rm ${API_CONTAINER} black src --check --diff
	@docker run --rm ${API_CONTAINER} pylint src
	@docker run --rm ${API_CONTAINER} mypy src
	@docker run --rm ${API_CONTAINER} pytest -s -vv


## OpenAPI
.PHONY: openapi.build
openapi.build:
	@docker build \
		-f $(OPENAPI_FOLDER)/Dockerfile \
		-t $(OPENAPI_CONTAINER) ./openapi

.PHONY: openapi.update
openapi.update:
	@docker run --rm \
		--name $(OPENAPI_CONTAINER) \
		--volume $(OPENAPI_COMPILED_FILE):/usr/src/app/openapi/compiled.yaml \
		$(OPENAPI_CONTAINER)

.PHONY: openapi.up
openapi.up:
	@docker-compose -f openapi/docker-compose.yml up

.PHONY: openapi.generate
openapi.generate:
	@docker run --rm \
		-v $(OPENAPI_FOLDER):/local \
		openapitools/openapi-generator-cli:v5.3.0 \
		generate \
		-i /local/compiled.yaml \
		-g typescript-axios \
		-o /local/api

##NEXT JS (REACT)
.PHONY: web.build
web.build:
	@docker build \
		-f $(WEB_FOLDER)/Dockerfile \
		-t $(WEB_CONTAINER) $(WEB_FOLDER)

.PHONY: web.install
web.install:
	@docker run --rm \
		--name $(WEB_CONTAINER) \
		--volume $(WEB_FOLDER):/usr/src/web:rw \
		$(WEB_CONTAINER) yarn install

.PHONY: web.up
web.up:
	@docker run --rm -it \
		--env-file $(ENVFILE_FOLDER)/.web \
		--net $(DOCKER_NETWORK) \
		--name $(WEB_CONTAINER) \
		--volume $(WEB_FOLDER):/usr/src/web:rw \
		--publish $(WEB_PORT):3000 \
		$(WEB_CONTAINER)

.PHONY: web.lint
web.lint:
	@docker run --rm \
		--name $(WEB_CONTAINER) \
		--volume $(WEB_CONTAINER):/usr/src/web:rw \
		$(WEB_CONTAINER) yarn run lint
	@docker run --rm \
		--name $(WEB_CONTAINER) \
		--volume $(WEB_CONTAINER):/usr/src/web:rw \
		$(WEB_CONTAINER) yarn run format
	

