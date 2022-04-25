#!/usr/bin/env bash

set -e
set -x
python manager.py db init
pytest --capture=no --cov=app --cov-report=term-missing app/tests "${@}"