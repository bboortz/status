import datetime

from app import app
from app import repo
from app.utils import get_current_time, config
from app.middleware import login_required

from flask import jsonify
from flask import request
from flask import abort



##
## *HTTP/REST methods*
##


#
# motd
#


# CURL: curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/motd 
# NO INPUT
# OUTPUT:
# {
#   "message": "works for you!", 
#   "updated": "2019-04-19 18:51:43 CEST"
# }
@app.route('/api/motd', methods=['GET'])
def read_motd():
	result = repo.motd
	return jsonify(result)


# CURL: curl -i -H "Content-Type: application/json" -X POST -d '{ "message": "OK" }' http://localhost:5000/api/motd 
# INPUT:
# {
#   "message": "OK"
# }'
# OUTPUT:
# {
#   "message": "OK", 
#   "updated": "2019-04-19 18:54:08 CEST"
# }
@app.route('/api/motd', methods=['POST', 'PUT'])
@login_required
def create_update_motd():
	# check input
	if not request.json or not 'message' in request.json:
		abort(400)

	# parse input
	message = request.json['message']

	if not isinstance(message, str):
		abort(400)

	# set item
	result = repo.setMotd(message)
	return jsonify(result), 201


# CURL: curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/motd
# NO INPUT
# OUTPUT:
# {
#   "deleted": true
# }
@app.route('/api/motd', methods=['DELETE'])
@login_required
def delete_motd():
	result = repo.deleteMotd()
	return jsonify(result)



#
# services
#


# CURL: curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/services
# NO INPUT
# OUTPUT:
# [
#   {
#     "name": "service0", 
#     "score": 100,
#     "updated": "2019-04-19 19:55:04 CEST"
#   }
# ]
@app.route('/api/services', methods=['GET'])
def get_services():
	result = repo.services
	return jsonify(result)


# CURL: curl -i -H "Content-Type: application/json" -X POST -d '{ "name": "service0", "score": 100 }' http://localhost:5000/api/service
# INPUT:
# {
#   "name": "service0", 
#   "score": 100 
# }
# OUTPUT:
# {
#   "name": "service0", 
#   "score": 100,
#   "updated": "2019-04-19 19:55:04 CEST"
# }
@app.route('/api/service', methods=['POST', 'PUT'])
@login_required
def create_update_service():
	# check input
	if not request.json or not 'name' in request.json or not 'score' in request.json:
		abort(400)

	# parse input
	name = request.json['name']
	score = request.json['score']

	if not isinstance(name, str) or not isinstance(score, int):
		abort(400)

	# set item
	result = repo.setService(name, score)
	return jsonify(result), 201


# CURL: curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/service/service0
# NO INPUT
# OUTPUT:
# {
#   "deleted": true
# }
@app.route('/api/service/<string:name>', methods=['DELETE'])
@login_required
def delete_service(name):
	result = repo.deleteService(name)

	if result == False:
		abort(404)

	return jsonify(result)



#
# events
#


# CURL: curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/events
# NO INPUT
# OUTPUT:
# [
#   {
#     "description": "test", 
#     "title": "service is online", 
#     "updated": "2019-04-19 20:33:09 CEST"
#   }
# ]
@app.route('/api/events', methods=['GET'])
def get_events():
	result = repo.events
	return jsonify(result)


# CURL: curl -i -H "Content-Type: application/json" -X POST -d '{ "title": "service is online", "description": "test" }' http://localhost:5000/api/event
# INPUT:
# {
#  "description": "test", 
#  "title": "service is online", 
# }
# OUTPUT:
# {
#  "description": "test", 
#  "title": "service is online", 
#  "updated": "2019-04-19 20:31:52 CEST"
# }
@app.route('/api/event', methods=['POST', 'PUT'])
@login_required
def post_event():
	# check input
	if not request.json or not 'title' in request.json or not 'description' in request.json:
		abort(400)

	# parse input
	title = request.json['title']
	description = request.json['description']

	if not isinstance(title, str) or not isinstance(description, str):
		abort(400)

	# set item
	result = repo.setEvent(title, description)
	return jsonify(result), 201


# CURL: curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/event/service%20is%20online
# NO INPUT
# OUTPUT:
# {
#   "deleted": true
# }
@app.route('/api/event/<string:title>', methods=['DELETE'])
@login_required
def delete_event(title):
	result = repo.deleteEvent(title)

	if result == False:
		abort(404)

	return jsonify(result)



#
# import
#

# CURL: ?
# INPUT:
# {
#     "motd": { 
#         "message":  "test0"
#     },
#     "services": [
#         { "name":  "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" }
#     ] },
#     "events": [
#         { "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" }
#     ] },
# }
# OUTPUT: ?
@app.route('/api/import', methods=['POST', 'PUT'])
@login_required
def post_import():
	# check input
	if not request.json:
		abort(400)
	if 'motd' in request.json:
		if len(request.json['motd']) >= 1:
			if not 'message' in request.json['motd']:
				abort(400)
			if not 'updated' in request.json['motd']:
				abort(400)

	found_items = []
	if 'services' in request.json:
		for service in request.json['services']:
			if len(service) >= 1:
				if not 'name' in service:
					abort(400)
				if not 'score' in service:
					abort(400)
				if not 'updated' in service:
					abort(400)

				key = service['name']
				if key in found_items:
					abort(400)
				found_items.append(key)

	found_items = []
	if 'events' in request.json:
		for event in request.json['events']:
			if len(event) >= 1:
				if not 'title' in event:
					abort(400)
				if not 'description' in event:
					abort(400)
				if not 'updated' in event:
					abort(400)

				key = event['title']
				if key in found_items:
					abort(400)
				found_items.append(key)
	
	
	# import data
	if 'motd' in request.json:
		repo.motd = request.json['motd']
	if 'services' in request.json:
		repo.services = request.json['services']
	if 'events' in request.json:
		repo.events = request.json['events']

	result = {
		"motd": repo.motd,
		"services": repo.services,
		"events": repo.events
	}
	return jsonify(result), 201



#
# export
#


# CURL: curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/export
# NO INPUT
# OUTPUT:
# {
#     "motd": { 
#         "message":  "test0"
#     },
#     "services": [
#         { "name":  "service0", "score": 99, "updated": "2019-04-19 13:57:42 CEST" }
#     ] },
#     "events": [
#         { "title": "event0", "description": "desc0", "updated": "2019-04-19 14:30:45 CEST" }
#     ] },
# }
@app.route('/api/export', methods=['GET'])
@login_required
def get_export():
	result = {
		"motd": repo.motd,
		"services": repo.services,
		"events": repo.events
	}
	return jsonify(result), 200
