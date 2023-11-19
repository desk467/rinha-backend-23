#!/bin/sh

gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker -b 0.0.0.0:8000 rinha.server:app
