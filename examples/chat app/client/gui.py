# -*- coding: utf-8 -*-
""" Definition of all GUI components. """
import wx

class loginDialog(wx.Dialog):

	def __init__(self, title="Login"):
		super(loginDialog, self).__init__(parent=None, id=wx.ID_ANY)
		self.SetTitle(title)
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		label1 = wx.StaticText(panel, wx.ID_ANY, "Username: ")
		self.username = wx.TextCtrl(panel, wx.ID_ANY, size=(380, -1))
		s = wx.BoxSizer(wx.HORIZONTAL)
		s.Add(label1, 0, wx.ALL, 5)
		s.Add(self.username, 0, wx.ALL, 5)
		sizer.Add(s, 0, wx.ALL, 5)
		label1 = wx.StaticText(panel, wx.ID_ANY, "Server: ")
		self.server = wx.TextCtrl(panel, wx.ID_ANY, "localhost", size=(380, -1))
		s = wx.BoxSizer(wx.HORIZONTAL)
		s.Add(label1, 0, wx.ALL, 5)
		s.Add(self.server, 0, wx.ALL, 5)
		sizer.Add(s, 0, wx.ALL, 5)
		label1 = wx.StaticText(panel, wx.ID_ANY, "Port: ")
		self.port = wx.SpinCtrl(panel, wx.ID_ANY, size=(380, -1))
		self.port.SetRange(1024, 65000)
		self.port.SetValue(33333)
		s = wx.BoxSizer(wx.HORIZONTAL)
		s.Add(label1, 0, wx.ALL, 5)
		s.Add(self.port, 0, wx.ALL, 5)
		sizer.Add(s, 0, wx.ALL, 5)

#		label2 = wx.StaticText(panel, wx.ID_ANY, "Password: ")
#		self.password = wx.TextCtrl(panel, wx.ID_ANY, size=(380, -1), style=wx.TE_PASSWORD)
#		ss = wx.BoxSizer(wx.HORIZONTAL)
#		ss.Add(label2, 0, wx.ALL, 5)
#		ss.Add(self.password, 0, wx.ALL, 5)
#		sizer.Add(ss, 0, wx.ALL, 5)
		ok = wx.Button(panel, wx.ID_OK, "Log in")
		ok.SetDefault()
		cancel = wx.Button(panel, wx.ID_CANCEL)
		self.SetEscapeId(wx.ID_CANCEL)
		bs = wx.BoxSizer(wx.HORIZONTAL)
		bs.Add(ok, 0, wx.ALL, 5)
		bs.Add(cancel, 0, wx.ALL, 5)
		sizer.Add(bs, 0, wx.ALL, 5)
		panel.SetSizer(sizer)
		self.SetClientSize(sizer.CalcMin())

class appFrame(wx.Frame):
	menu_items = [
			("create_room", "Create new room"),
			("join_room", "Join a room")
		]
	secondary_menu_items = list()

	def __init__(self):
		super(appFrame, self).__init__(parent=None, title="Chat Window")
		self.Maximize(True)
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sb = self.CreateStatusBar()
		lbl = wx.StaticText(self.panel, wx.ID_ANY, "menu")
		self.list = wx.ListBox(self.panel, wx.ID_ANY)
		self.sizer.Add(lbl, 0, wx.GROW)
		self.sizer.Add(self.list, 1, wx.GROW)
		lbl = wx.StaticText(self.panel, -1, "Chat")
		self.chat = wx.TextCtrl(self.panel, -1)
		self.chat.Enable(False)
		sizerchat = wx.BoxSizer(wx.HORIZONTAL)
		sizerchat.Add(lbl, 0, wx.ALL, 5)
		sizerchat.Add(self.chat, 0, wx.ALL, 5)
		self.sizer.Add(sizerchat, 0, wx.ALL, 5)
		lbl1 = wx.StaticText(self.panel, wx.ID_ANY, "History")
		self.history = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_MULTILINE, size=(500, 300))
		self.history.Enable(False)
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(lbl1, 0, wx.ALL, 5)
		box.Add(self.history, 0, wx.ALL, 5)
		self.sizer.Add(box, 0, wx.ALL, 5)
		self.panel.SetSizerAndFit(self.sizer)

	def get_item(self):
		return self.list.GetSelection()

	def add_message(self, message, reverse=False):
		old_line = self.history.GetNumberOfLines()
		point = self.history.GetInsertionPoint()
		if reverse:
			self.history.SetValue(message+"\n"+self.history.GetValue())
		else:
			self.history.AppendText(message+"\n")
		self.history.SetInsertionPoint(point)
		new_line = self.history.GetNumberOfLines()#.count("\n")
		return (old_line, new_line)

	def enable_app(self):
		for i in self.menu_items:
			self.list.Append(i[1])
		self.chat.Enable(True)
		self.history.Enable(True)

	def  show_connection_error(self):
		msg = wx.MessageDialog(None, "Connection error. Try again", "error", style=wx.ICON_ERROR).ShowModal()