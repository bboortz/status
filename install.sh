#!/bin/sh


if [ ! -f /.dockerenv ]; then
	python -m venv .venv
	source .venv/bin/activate
fi
pip install -U -r requirements.txt
