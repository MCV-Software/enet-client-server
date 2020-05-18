# -*- coding: utf-8 -*-
import sys
import threading
import wx
import client
import output
import gui
import sound
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
		self.next_action = ""

	def connect_events(self):
		self.window.chat.Bind(wx.EVT_CHAR_HOOK, self.on_process)
		self.window.list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_process_listbox_click)
		self.window.list.Bind(wx.EVT_CHAR_HOOK, self.on_process_listbox)
		pub.subscribe(self.response, "response")
		pub.subscribe(self.ask_login, "ask_login")
		pub.subscribe(self.disconnected, "disconnected")

	def on_process(self, event):
		key = event.GetKeyCode()
		if key == wx.WXK_RETURN:
			self.send_message()
		event.Skip()

	def on_process_listbox_click(self, event):
		selected_option = self.window.menu_items[self.window.list.GetSelection()][0]
		if selected_option == "create_room":
			data = dict(action="create_room")
			c.send_data(0, data)
		elif selected_option == "join_room":
			data = dict(action="request_room_list")
			c.send_data(0, data)
		if event != None:
			event.Skip()

	def on_process_listbox(self, event):
		key = event.GetKeyCode()
		if key == wx.WXK_RETURN:
			self.on_process_listbox_click(None)
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
		self.window.enable_app()
		connected = data.get("nickname")
		msg = "{} has entered this platform".format(connected)
		self.window.add_message(msg)

	def cmd_message(self, data):
		msg = data.get("message")
		nickname = data.get("nickname")
		msg = "{0}: {1}".format(nickname, msg)
		output.speak(msg)
		sound.sound.play("chat.ogg")
		self.window.add_message(msg)

	def cmd_create_room(self, data):
		self.window.list.Clear()
		msg = "{} Has created a room.".format(data.get("nickname"))
		self.window.add_message(msg)
		output.speak(msg)

	def cmd_room_list(self, data):
		print(data)


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
	sound.setup()
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