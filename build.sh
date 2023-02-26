#!/usr/bin/env bash
# exit on error
set -o errexit
# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs -d '\n')
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate