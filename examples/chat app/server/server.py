import string
import random
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

    def cmd_create_room(self, data):
        code = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
        existing = True
        while existing:
            existing = self.server.room_exists(code)
            if existing == True:
                code = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
        self.server.rooms.append(code)
        data.update(nickname=self.nickname)
        self.room = code
        self.send_data(0, data)

    def cmd_request_room_list(self, data):
        rooms = dict()
        for room in self.server.rooms:
            players = self.server.get_players_in_room(room)
            rooms[room]= players
        self.send_data(0, dict(action="room_list", rooms=rooms))

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

    def room_exists(self, room_id):
        for i in self.rooms:
            if room_id == i:
                return True
        return False

    def get_players_in_room(self, room_id):
        return [player.nickname for player in self.peers if player.room == room_id]

if __name__ == "__main__":
    print("Starting chat server...")
    s = server()
    s.run()
