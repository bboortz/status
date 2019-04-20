
import pytest
import json

from app.utils import config



x_api_key = config['api_key']



@pytest.fixture(params=[
	{ "message":  "test0" },
	{ "message":  "test1" },
	{ "message":  "test2" }
	])
def motd_request_dict_positive(request):
	return request.param


@pytest.fixture(params=[
	{ "message":  1 },
	{ "messagewrong":  "test0" },
	{ }
	])
def motd_request_dict_negative(request):
	return request.param


@pytest.fixture(params = [ 
	{ "name":  "service0", "score": 99 },
	{ "name":  "service1", "score": -10 },
	{ "name":  "service1", "score": 10 },
	{ "name":  "service2", "score": 100 }
	])
def service_request_dict_positive(request):
	return request.param


@pytest.fixture(params = [ 
	{ "name":  "servicewrong", "score": "99" },
	{ "name":  1, "score": 99 },
	{ "name":  "servicewrong" },
	{ "score": 99 },
	{ }
	])
def service_request_dict_negative(request):
	return request.param


@pytest.fixture(params = [ 
	{ "title":  "event0", "description": "desc0" },
	{ "title":  "event1", "description": "desc1" },
	{ "title":  "event1", "description": "desc1" },
	{ "title":  "event2", "description": "desc2" }
	])
def event_request_dict_positive(request):
	return request.param


@pytest.fixture(params = [ 
	{ "title":  "event0", "descritionwrong": "desc0" },
	{ "titlewrong":  "event0", "description": "desc0" },
	{ "title":  "event0" },
	{ "description": "desc0" },
	{ }
	])
def event_request_dict_negative(request):
	return request.param


@pytest.fixture(params = [ 
	{ "motd": { } },
	{ "motd": { "message":  "test0", "updated": "2019-04-19 13:57:42 CEST" } },
	{ "services": [ ] },
	{ "services": [ { "name": "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" } ] },
	{ "services": [ 
		{ "name": "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" },
		{ "name": "service1", "score": 99, "updated": "2019-04-19 13:57:42 CEST" }
	] },
	{ "events": [ ] },
	{ "events":   [ { "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" } ] },
	{ "events":   [ 
		{ "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" },
		{ "title": "event1", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" }
	] },
	{
		"motd": { "message":  "test0", "updated": "2019-04-19 13:57:42 CEST" },
		"services": [ { "name":  "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" } ]
	},
	{
		"motd": { "message":  "test0", "updated": "2019-04-19 13:57:42 CEST" },
		"events": [ { "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" } ]
	},
	{ 
		"services": [ { "name":  "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" } ], 
		"events": [ { "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" } ]
	},
	{ 
		"motd": { "message":  "test0", "updated": "2019-04-19 13:57:42 CEST" },
		"services": [ { "name":  "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" } ], 
		"events": [ { "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" } ]
	}
	])
def import_request_dict_positive(request):
	return request.param


@pytest.fixture(params = [ 
	{ "motd": { "messagewrong":  "test0", "updated": "2019-04-19 13:57:42 CEST" } },
	{ "services": [ { "name":  "service0", "score": 99 } ] },
	{ "services": [ { "name":  "service0", "updated": "2019-04-19 13:57:42 CEST" } ] },
	{ "services": [ { "name":  "service0", "score": 99 } ] },
	{ "services": [ { "namewrong":  "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" } ] },
	{ "services": [ { "name":  "service0", "scorewrong": 99, "updated": "2019-04-19 13:57:42 CEST" } ] },
	{ "services": [ { "name":  "service0", "score": 99, "updatedwrong": "2019-04-19 13:57:42 CEST" } ] },
	{ "services": [ 
		{ "name": "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" },
		{ "name": "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" }
	] },
	{ "events":   [ 
		{ "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" },
		{ "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" }
	] },
	{ }
	])
def import_request_dict_negative(request):
	return request.param



@pytest.mark.api
@pytest.mark.motd
def test_create_or_update_motd(client, motd_request_dict_positive):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/motd', data=json.dumps(motd_request_dict_positive), content_type='application/json', headers=headers)
	assert "201 CREATED" == rv.status
	result_dict = json.loads(rv.data)
	assert 'test' in result_dict['message']


@pytest.mark.api
@pytest.mark.motd
def test_create_or_update_motd_negative(client, motd_request_dict_negative):
	"""Testing the API"""

	rv = client.post('/api/motd', content_type='application/json')
	assert "403 FORBIDDEN" == rv.status

	headers = { 'X-API-KEY': "wrongApiKey" }
	rv = client.post('/api/motd', content_type='application/json', headers=headers)
	assert "403 FORBIDDEN" == rv.status

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/motd', content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/motd', data=json.dumps(motd_request_dict_negative), content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status


@pytest.mark.api
@pytest.mark.motd
def test_get_motd1(client):
	"""Testing the API"""

	rv = client.get('/api/motd')
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	assert 'test2' == result_dict['message']


@pytest.mark.api
@pytest.mark.motd
def test_delete_motd(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.delete('/api/motd', content_type='application/json', headers=headers)
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	assert True == result_dict['deleted']


@pytest.mark.api
@pytest.mark.motd
def test_delete_motd_negative(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.delete('/api/motd/1', content_type='application/json', headers=headers)
	assert "404 NOT FOUND" == rv.status


@pytest.mark.api
@pytest.mark.motd
def test_get_motd2(client):
	"""Testing the API"""

	rv = client.get('/api/motd')
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	assert 'messages' not in result_dict
	assert 'updated' in result_dict


@pytest.mark.api
@pytest.mark.service
def test_create_or_update_service(client, service_request_dict_positive):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/service', data=json.dumps(service_request_dict_positive), content_type='application/json', headers=headers)
	assert "201 CREATED" == rv.status
	result_dict = json.loads(rv.data)
	assert 'name' in result_dict
	assert 'score' in result_dict
	assert 'updated' in result_dict


@pytest.mark.api
@pytest.mark.service
def test_create_or_update_service_negative(client, service_request_dict_negative):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/service', content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/service', data=json.dumps(service_request_dict_negative), content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status


@pytest.mark.api
@pytest.mark.service
def test_get_services1(client):
	"""Testing the API"""

	rv = client.get('/api/services')
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	length = len(result_dict)
	print(result_dict)
	assert length == 3

	for i in range(0, length -1):
		service = result_dict[i]
		assert 'name' in service
		assert 'score' in service
		assert 'updated' in service


@pytest.mark.api
@pytest.mark.service
def test_delete_service(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.delete('/api/service/service2', content_type='application/json', headers=headers)
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	assert True == result_dict['deleted']


@pytest.mark.api
@pytest.mark.service
def test_delete_service_negative(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.delete('/api/service/5', content_type='application/json', headers=headers)
	assert "404 NOT FOUND" == rv.status


@pytest.mark.api
@pytest.mark.service
def test_get_service2(client):
	"""Testing the API"""

	rv = client.get('/api/services')
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	length = len(result_dict)
	print(result_dict)
	assert length == 2

	for i in range(0, length -1):
		service = result_dict[i]
		assert 'name' in service
		assert 'score' in service
		assert 'updated' in service


@pytest.mark.api
@pytest.mark.event
def test_create_or_update_event(client, event_request_dict_positive):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/event', data=json.dumps(event_request_dict_positive), content_type='application/json', headers=headers)
	assert "201 CREATED" == rv.status
	result_dict = json.loads(rv.data)
	assert 'title' in result_dict
	assert 'description' in result_dict
	assert 'updated' in result_dict


@pytest.mark.api
@pytest.mark.event
def test_create_or_event_service_negative(client,event_request_dict_negative):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/event', content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/service', data=json.dumps(event_request_dict_negative), content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status


@pytest.mark.api
@pytest.mark.event
def test_get_events1(client):
	"""Testing the API"""

	rv = client.get('/api/events')
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	length = len(result_dict)
	print(result_dict)
	assert length == 3

	for i in range(0, length -1):
		event = result_dict[i]
		assert 'title' in event
		assert 'description' in event
		assert 'updated' in event


@pytest.mark.api
@pytest.mark.event
def test_delete_event(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.delete('/api/event/event2', content_type='application/json', headers=headers)
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	assert True == result_dict['deleted']


@pytest.mark.api
@pytest.mark.event
def test_delete_event_negative(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.delete('/api/event/5', content_type='application/json', headers=headers)
	assert "404 NOT FOUND" == rv.status


@pytest.mark.api
@pytest.mark.event
def test_get_events2(client):
	"""Testing the API"""

	rv = client.get('/api/events')
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	length = len(result_dict)
	print(result_dict)
	assert length == 2

	for i in range(0, length -1):
		event = result_dict[i]
		assert 'title' in event
		assert 'description' in event
		assert 'updated' in event


@pytest.mark.api
@pytest.mark.data
def test_import(client, import_request_dict_positive):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/import', data=json.dumps(import_request_dict_positive), content_type='application/json', headers=headers)
	assert "201 CREATED" == rv.status
	result_dict = json.loads(rv.data)
	if 'motd' in import_request_dict_positive:
		assert import_request_dict_positive['motd'] == result_dict['motd']
	assert 'services' in result_dict
	if 'services' in import_request_dict_positive:
		assert import_request_dict_positive['services'] == result_dict['services']
	assert 'events' in result_dict
	if 'events' in import_request_dict_positive:
		assert import_request_dict_positive['events'] == result_dict['events']


@pytest.mark.api
@pytest.mark.data
def test_import_negative(client, import_request_dict_negative):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/import', content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status

	headers = { 'X-API-KEY': x_api_key }
	rv = client.post('/api/import', data=json.dumps(import_request_dict_negative), content_type='application/json', headers=headers)
	assert "400 BAD REQUEST" == rv.status


@pytest.mark.api
@pytest.mark.data
@pytest.mark.export
def test_export(client):
	"""Testing the API"""

	headers = { 'X-API-KEY': x_api_key }
	rv = client.get('/api/export', headers=headers)
	assert "200 OK" == rv.status
	result_dict = json.loads(rv.data)
	assert 'motd' in result_dict
	assert 'services' in result_dict
	assert 'events' in result_dict


