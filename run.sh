#!/bin/sh


HOST=0.0.0.0
PORT=5000

export FLASK_APP=status.py

if [ ! -f /.dockerenv ]; then
	source .venv/bin/activate
fi



if [ -n "${DEV:-}" ] ; then
	export FLASK_ENV=development
	export FLASK_DEBUG=1
	flask run --host ${HOST} --port ${PORT}
else
	export FLASK_ENV=production
	export FLASK_DEBUG=1
	gunicorn --workers 4 -b ${HOST}:${PORT} status:app
fi

