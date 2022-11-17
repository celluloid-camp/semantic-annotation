#!/bin/sh
set -e

python3 -c <<EOF |
from django.db import IntegrityError
try:
    python3 manage.py install_labels
except IntegrityError:
    print(“Already installed”)
EOF
python3 manage.py migrate # Apply database migrations

python3 manage.py runserver 0.0.0.0:8000