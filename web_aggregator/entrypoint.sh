#!/bin/sh
export FLASK_APP=wsgi.py
export FLASK_DEBUG=0
flask run --host=0.0.0.0 --port 5005
