from enetcomponents import server

class channel(server.channel):

	def __init__(self, *args, **kwargs):
		super(channel, self).__init__(*args, **kwargs)
		self.nickname = None

	def network(self, event, data):
		f = data.get("action")
		if f == None:
			print("Error: Invalid data in protocol. %r" % (data))
			return
		if hasattr(self, "cmd_"+f) == False:
			print("Error: function cmd_{} does not exist".format(f))
			return
		getattr(self, "cmd_"+f)(data)

	def cmd_login(self, data):
		nickname = data.get("nickname")
		self.nickname = nickname
		self.room = "public"
		d = dict(action="connected", nickname=nickname)
		self.server.send_to_all(0, d)

	def cmd_send_message(self, data):
		data.update(nickname=self.nickname, action="message")
		for channel in self.server.peers:
			if channel.room == self.room:
				channel.send_data(0, data)

class server(server.server):

	def __init__(self, *args, **kwargs):
		super(server, self).__init__(*args, **kwargs)
		self.rooms = list()

	def connected(self, peer):
		p = channel(self, peer)
		self.peers[p] = True

	def disconnected(self, peer):
		for channel in self.peers:
			if peer.incomingPeerID == channel.peer.incomingPeerID:
				del self.peers[channel]
				break

if __name__ == "__main__":
	print("Starting chat server...")
	s = server()
	s.run()