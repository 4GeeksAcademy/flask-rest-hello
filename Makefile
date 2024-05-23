# Makefile

ALEMBIC=alembic -c migrations/alembic.ini

# Include environment variables if .env file exists
ifneq (,$(wildcard $(ENV)))
	include $(ENV)
	export $(shell sed 's/=.*//' $(ENV))
endif

install:
	pipenv install --deploy --ignore-pipfile

# start dev server on production
web:
	pipenv run uvicorn main:app --chdir ./src/

# Apply all migrations
.PHONY: upgrade
upgrade:
	$(ALEMBIC) upgrade head

# Create a new migration (revision message is required)
.PHONY: migrate
migrate:
	@read -p "Enter migration message: " msg; \
	$(ALEMBIC) revision --autogenerate -m "$$msg"

# Downgrade the last migration
.PHONY: downgrade
downgrade:
	$(ALEMBIC) downgrade -1