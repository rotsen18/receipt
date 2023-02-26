#!/usr/bin/env bash
# exit on error
set -o errexit
# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs -d '\n')
python -m pip install --upgrade pip
pip3 install -r requirements.txt

python3 manage.py collectstatic --no-input
python3 manage.py migrate