#!/bin/bash

echo "running migrations commands..."

python3 -m alembic revision --autogenerate -m "create inital tables"
python3 -m alembic upgrade head

echo "applied migrations!"