#!/bin/sh
source .venv/bin/activate
FLASK_APP=./api/api.py flask --debug run -h 0.0.0.0

#need to add frontend server aswell 
