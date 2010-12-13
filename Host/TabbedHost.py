# See LICENCE for the source code licence.
# (c) 2010 Dan Saul

import sys,os,argparse
import gobject,pygtk,gtk,gio
import dbus,dbus.service,dbus.mainloop.glib
from HostClient import HostClient
from UnsavedChangesHandler import UnsavedChangesHandler
from ComponentHostDBus import ComponentHostDBus
from Components import Client,Host

class TabbedHost(object):
	bus = None
	bus_name = None
	bus_service_name = None
	bus_obj = None
	
	glade_prefix = ""
	
	builder = None
	window = None
	
	entry = None
	button = None
	
	notebook = None
	embed = None
	
	clients = []
	
	def __init__(self,add_pid):
		super(TabbedHost, self).__init__()
		assert add_pid >= 0
		
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		self.bus = dbus.SessionBus()
		self.bus_name = Host.BUS_INTERFACE_NAME+"_"+str(os.getpid())
		self.bus_service_name = dbus.service.BusName(self.bus_name, self.bus)
		self.bus_obj = ComponentHostDBus(self.bus, Host.BUS_OBJECT_PATH, self)
		
		assert self.bus != None
		assert self.bus_name != None
		assert self.bus_service_name != None
		assert self.bus_obj != None
		
		try:
			self.glade_prefix = os.environ["GLADE_PREFIX"]
		except KeyError:
			print "No Glade Environment"
		
		self.builder = gtk.Builder()
		path = self.glade_prefix+"TabbedHost.glade"
		assert os.path.exists(path)
		self.builder.add_from_file(path)
		
		self.window = self.builder.get_object("window")
		self.notebook = self.builder.get_object("notebook")
		
		assert self.window != None
		assert self.notebook != None
		
		self.window.connect("delete-event",self.do_window_delete_event)
		self.window.show_all()
		
		if add_pid != 0:
			self.add_pid(add_pid)
		pass
	
	__uch = None
	def do_window_delete_event(self,sender,event):
		deny_close = False
		clients_denying_close = []
		
		# Check for any clients that can't just be closed.
		for client in self.clients:
			d = client.GetSaveStatus()
			if d != Client.SAVE_STATUS_SAVED:
				clients_denying_close.append(client)
				deny_close = True
		
		self.__uch = UnsavedChangesHandler(clients_denying_close,self)
		self.__uch.show(self.window)
		
		print "deny_close",deny_close
		if deny_close:
			return True # Stop Delete
		
		# Tell all the clients to quit.
		for client in self.clients:
			client.NotifyClosedByHost()
		
		gtk.main_quit()
		return False
	
	def unsaved_changes_handler_return(self,resolution):
		print "unsaved_changes_handler_return",resolution
		self.__uch = None
		pass
	
	def update_save_status(self,client,status):
		if self.__uch:
			self.__uch.update_save_status(client,status)
	
	def do_add_pid_clicked(self,sender):
		self.add_pid(int(self.entry.get_text()))
	
	def add_pid(self,pid):
		client = HostClient(self.bus,pid,self)
		self.clients.append(client)
		
		hbox = gtk.HBox(spacing=5)
		hbox.pack_start(client.image,expand=False,fill=False)
		hbox.pack_start(client.label,expand=True,fill=True)
		hbox.pack_start(client.closebutton,expand=False,fill=False)
		hbox.show_all()
		
		self.notebook.append_page(client.widget,hbox)
	
	def remove_pid(self,pid):
		for client in self.clients:
			self.notebook.remove_page(self.notebook.page_num(client.widget))
			del client

	

