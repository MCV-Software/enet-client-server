# -*- coding: utf-8 -*-
import time
import json
import enet

class client(object):

	def __init__(self, host=b"localhost", port=33333, peer_count=1, channel_limit=4, incoming_bandwidth=0, outgoing_bandwidth=0):
		self.host = enet.Host(None, peer_count, channel_limit, incoming_bandwidth, outgoing_bandwidth)
		address = enet.Address(host, port)
		self.peer = self.host.connect(address, channel_limit)

	def run(self):
		running = True
		while running:
			event = self.host.service(0)
			if event.type == enet.EVENT_TYPE_CONNECT:
				print("%s: CONNECT" % event.peer.address)
			elif event.type == enet.EVENT_TYPE_DISCONNECT:
				print("%s: DISCONNECT" % event.peer.address)
			elif event.type == enet.EVENT_TYPE_RECEIVE:
				print("%s: IN:  %r" % (event.peer.address, event.packet.data))
			time.sleep(0.001)

	def send_data(self, channel, data, reliable=True):
		data_str = json.dumps(data, ensure_ascii=False)
		data_bytes = bytes(data_str, "utf-8")
		if reliable:
			flags = enet.PACKET_FLAG_RELIABLE
		else:
			flags = enet.PACKET_FLAG_UNSEQUENCED
		packet = enet.Packet(data_bytes, flags)
		self.peer.send(channel, packet)

	def disconnect(self):
		self.peer.disconnect()

	def __del__(self):
		del self.host
		del self.peer