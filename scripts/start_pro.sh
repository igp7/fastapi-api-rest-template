#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/database/scripts/check_active_database.py

# Create initial data in DB
python app/database/scripts/initial_data.py

# Init fastapi pro
fastapi run --workers 4 app/main.py --port 8000