# -*- coding: utf-8 -*-
import sys
import threading
import wx
import client
import output
import gui
from pubsub import pub

# Client instance.
c = None

# thread to keep the client running.
t = None

class controller(object):
	def __init__(self, window):
		super(controller, self).__init__()
		self.window = window
		self.connect_events()
		self.window.Show()

	def connect_events(self):
		self.window.chat.Bind(wx.EVT_CHAR_HOOK, self.on_process)
		pub.subscribe(self.response, "response")
		pub.subscribe(self.ask_login, "ask_login")
		pub.subscribe(self.disconnected, "disconnected")

	def on_process(self, event):
		key = event.GetKeyCode()
		if key == wx.WXK_RETURN:
			self.send_message()
		event.Skip()

	def send_message(self):
		global c
		message = self.window.chat.GetValue()
		if message == "" or message == None:
			return wx.Bell()
		# Otherwise, message does exist.
		data = dict(action="send_message", message=message)
		c.send_data(0, data)
		self.window.chat.ChangeValue("")

	def response(self, data):
		command = data.get("action")
		if hasattr(self, "cmd_"+command):
			getattr(self, "cmd_"+command)(data)

	def cmd_connected(self, data):
		connected = data.get("nickname")
		msg = "{} has entered this platform".format(connected)
		self.window.add_message(msg)

	def cmd_message(self, data):
		msg = data.get("message")
		nickname = data.get("nickname")
		msg = "{0}: {1}".format(nickname, msg)
		output.speak(msg)
		self.window.add_message(msg)

	def ask_login(self):
		global c
		data = dict(action="login", nickname=self.username)
		c.send_data(0, data)

	def disconnected(self):
		self.window.show_connection_error()
		wx.GetApp().ExitMainLoop()

def setup():
	global c, t
	output.setup()
	app = wx.App()
	d = gui.loginDialog()
	f = gui.appFrame()
	mainController = controller(f)
	if d.ShowModal() != wx.ID_OK:
		return
	username = d.username.GetValue()
	server = bytes(d.server.GetValue(), "utf-8")
	port = int(d.port.GetValue())
	mainController.username = username
	d.Destroy()
	c = client.client(host=server, port=port)
	t = threading.Thread(target=c.run)
	t.start()
	app.MainLoop()
	c.close()

setup()