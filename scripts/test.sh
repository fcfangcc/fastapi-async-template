#!/usr/bin/env bash

set -e
set -x
poetry run pytest --capture=no --cov=app --cov-report=term-missing app/tests "${@}"
