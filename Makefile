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

# Remove an restart de database
.PHONY: init
init:
	$(ALEMBIC) init migrations
	@cp .devcontainer/migrations/alembic.ini migrations/alembic.ini
	@cp .devcontainer/migrations/env.py migrations/env.py
	@echo "Copied custom alembic.ini and env.py to migrations directory."
	@echo "Database and migrations initialized successfully."

# Remove an restart de database
.PHONY: restart_db
restart_db:
	@echo "Restarting database and initializing migrations..."
	@if [ -d "migrations" ]; then \
		rm -rf migrations; \
		echo "Removed existing migrations directory."; \
	fi
	@$(ALEMBIC) init migrations
	@echo "Reinitialized alembic in migrations directory."
	@if [ ! -f ".devcontainer/migrations/alembic.ini" ] || [ ! -f ".devcontainer/migrations/env.py" ]; then \
		echo "Error: .devcontainer/migrations/alembic.ini or .devcontainer/migrations/env.py not found."; \
		exit 1; \
	fi
	@cp .devcontainer/migrations/alembic.ini migrations/alembic.ini
	@cp .devcontainer/migrations/env.py migrations/env.py
	@echo "Copied custom alembic.ini and env.py to migrations directory."
	@echo "Database and migrations initialized successfully."

	@if psql -lqt -h localhost -U gitpod | cut -d \| -f 1 | grep -qw example; then \
		dropdb -h localhost -U gitpod example; \
		echo "Dropped existing database 'example'."; \
	else \
		echo "Database 'example' does not exist."; \
	fi

	createdb -h localhost -U gitpod example || true && \
	psql -h localhost example -U gitpod -c 'CREATE EXTENSION unaccent;' || true && \
	$(ALEMBIC) revision --autogenerate && \
	$(ALEMBIC) upgrade head