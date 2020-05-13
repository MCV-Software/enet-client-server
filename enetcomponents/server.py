import enet
import time
import json

class channel(object):

	def __init__(self, server, peer):
		self.peer = peer
		self.server = server

	def send_data(self, channel, data, reliable=True):
		data_str = json.dumps(data, ensure_ascii=False)
		data_bytes = bytes(data_str, "utf-8")
		if reliable:
			flags = enet.PACKET_FLAG_RELIABLE
		else:
			flags = enet.PACKET_FLAG_UNSEQUENCED
		packet = enet.Packet(data_bytes, flags)
		self.peer.send(channel, packet)

	def network(self, event, data):
		print(data)

	def disconnect(self):
		self.peer.disconnect()

class server(object):

	def __init__(self, host=b"localhost", port=33333, peer_count=256, channel_limit=4, incoming_bandwidth=0, outgoing_bandwidth=0):
		address = enet.Address(host, port)
		self.host = enet.Host(address, peer_count, channel_limit, incoming_bandwidth, outgoing_bandwidth)
		self.peers = {}

	def run(self):
		self.running = True
		while self.running:
			event = self.host.service(0)
			if event.type == enet.EVENT_TYPE_CONNECT:
				self.connected(event.peer)
			elif event.type == enet.EVENT_TYPE_DISCONNECT:
				self.disconnected(event.peer)
			elif event.type == enet.EVENT_TYPE_RECEIVE:
				channel_object = self.get_channel(event.peer)
				if channel_object == None:
					print("Error receiving packet for invalid channel: %r" % (event.data))
					return
				data = event.packet.data
				data_dict = json.loads(data, encoding="utf-8")
				channel_object.network(event, data_dict)
			time.sleep(0.0001)

	def get_channel(self, peer):
		for channel in self.peers:
			if peer.incomingPeerID == channel.peer.incomingPeerID:
				return channel

	def connected(self, peer):
		p = channel(self, peer)
		self.peers[p] = True
		print(len(self.peers))
		p.send_data(0, dict(action="connected"), False)
		print("%s: CONNECTED" % peer.address)

	def disconnected(self, peer):
		for channel in self.peers:
			if peer.incomingPeerID == channel.peer.incomingPeerID:
				del self.peers[channel]
				print("%s: DISCONNECT" % peer.address)
				break

	def send_to_all(self, channel, data, reliable=True):
		data_str = json.dumps(data, ensure_ascii=False)
		data_bytes = bytes(data_str, "utf-8")
		if reliable:
			flags = enet.PACKET_FLAG_RELIABLE
		else:
			flags = enet.PACKET_FLAG_UNSEQUENCED
		packet = enet.Packet(data_bytes, flags)
		self.host.broadcast(channel, packet)

	def close(self):
		self.running = False

	def __del__(self):
		del self.host