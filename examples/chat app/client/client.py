# -*- coding: utf-8 -*-
""" client communication for this simple chat example application.
This is a class derived from enetcomponents.client.client, which sends all data over pubsub via the topic response.
"""
from enetcomponents import client
from pubsub import pub

class client(client.client):

	def network(self, event, data):
		""" This functions receives data from an enet server in the following protocol:
		dict(action="some_command", **kwargs)
		This function will send all data to whatever listener in the pubsub stack by using the topic "response".
	"""
		f = data.get("action")
		if f == None:
			print("Error: Invalid data in protocol. %r" % (data))
			return
		pub.sendMessage("response", data=data)

	def connected(self, peer):
		pub.sendMessage("ask_login")

	def disconnected(self, peer):
		pub.sendMessage("disconnected")

