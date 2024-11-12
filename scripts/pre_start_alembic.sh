#! /usr/bin/env bash

set -e
set -x

export PYTHONPATH=.

# Let the DB start
python app/database/scripts/check_active_database.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/database/scripts/initial_data.py
