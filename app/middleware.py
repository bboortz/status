
import datetime

from app import app
from app import repo
from app.utils import get_current_time, config

from functools import wraps
from flask import g, request, redirect, url_for
from flask import jsonify
from flask import request
from flask import render_template
from flask import abort

from markupsafe import Markup



##
## *Flask Middleware
##

#
# API Authentication
#


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'X-API-KEY' not in request.headers:
			abort(403)

		expected_api_key = config['api_key']
		x_api_key = request.headers['X-API-KEY']

		if x_api_key != expected_api_key:
			abort(403)
		return f(*args, **kwargs)
	return decorated_function
