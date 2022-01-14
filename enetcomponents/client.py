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
        self.running = True
        while self.running:
            event = self.host.service(0)
            if event.type == enet.EVENT_TYPE_CONNECT:
                if hasattr(self, "connected"):
                    self.connected(event.peer)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                if hasattr(self, "disconnected"):
                    self.disconnected(event.peer)
            elif event.type == enet.EVENT_TYPE_RECEIVE:
                data = event.packet.data
                data_dict = json.loads(data)
                self.network(event, data_dict)
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

    def network(self, event, data):
        print(data)

    def disconnect(self):
        self.peer.disconnect()

    def close(self):
        self.running = False

    def __del__(self):
        del self.host
        del self.peer
