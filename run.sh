#!/bin/bash
# Django development server startup script
# Usage: ./run.sh

conda run -n antigravity python manage.py runserver 0.0.0.0:8123
