
import json

from app.utils import get_current_time, config




class Repository:

	def __init__(self):
		self.motd = { "message": "works for you!", "updated": get_current_time() }
		self.services = [ ]
		self.events = [ ]

	
	def __add_or_update_item(self, list, item, item_key):
		# find item to update
		update_id = -1
		for i, s in enumerate(list):
			key_value = item[item_key]
			if s[item_key] == key_value:
				update_id = i
				break

		# write item
		if update_id != -1:
			list[update_id] = item
		else:
			list.append(item)


	def setMotd(self, message):
		self.motd = { "message": message, "updated": get_current_time() }
		return self.motd


	def deleteMotd(self):
		self.motd = { "updated": get_current_time() }
		return { "deleted": True }


	def setService(self, name, score):
		# build item
		now = get_current_time()
		service = {
			'name': name,
			'score': score,
			'updated': now
		}

		# set item
		self.__add_or_update_item(self.services, service, "name")

		return service


	def deleteService(self, name):
		# find item to delete
		service = [service for service in self.services if service['name'] == name]
		if len(service) == 0:
			return False

		self.services.remove(service[0])

		return { "deleted": True }


	def setEvent(self, title, description):
		# build item
		now = get_current_time()
		event = {
			'title': title,
			'description': description,
			'updated': now
		}

		# set item
		self.__add_or_update_item(self.events, event, "title")

		return event


	def deleteEvent(self, title):
		# find item to delete
		event = [event for event in self.events if event['title'] == title]
		if len(event) == 0:
			return False

		self.events.remove(event[0])

		return { "deleted": True }
