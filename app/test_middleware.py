import os
import tempfile
import pytest
import json

from app import app
from app.utils import config
from app.middleware import login_required

from flask import jsonify

from markupsafe import Markup



x_api_key = config['api_key']



@app.route('/secret_page')
@login_required
def secret_page():
	result = { "result": "success" }
	return jsonify(result)


@pytest.mark.middleware
@pytest.mark.login
def test_login_positive(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.get('/secret_page', headers=headers)
	assert "200 OK" == rv.status


@pytest.mark.middleware
@pytest.mark.login
def test_login_negative(client):
	"""Testing the API"""

	rv = client.get('/secret_page')
	assert "403 FORBIDDEN" == rv.status

	headers = { 'X-API-KEY': "wrongApiKey" }
	rv = client.get('/secret_page', headers=headers)
	assert "403 FORBIDDEN" == rv.status
