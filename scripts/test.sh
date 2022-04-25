#!/usr/bin/env bash

set -e
set -x

pytest --capture=no --cov=app --cov-report=term-missing app/tests "${@}"