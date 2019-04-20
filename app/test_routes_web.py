
import pytest



@pytest.mark.web
def test_index(client):
	"""Testing the API"""

	rv = client.get('/')
	assert "200 OK" == rv.status
	assert b'Statusboard' in rv.data


@pytest.mark.web
def test_not_found(client):
	"""Testing the API"""

	rv = client.get('/aa')
	assert "404 NOT FOUND" == rv.status
	assert b'Not Found' in rv.data
