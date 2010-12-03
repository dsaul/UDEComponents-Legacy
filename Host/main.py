# See LICENCE for the source code licence.
# (c) 2010 Dan Saul

import sys,os,argparse
import gobject,pygtk,gtk,gio
import dbus,dbus.service,dbus.mainloop.glib
from HostClient import Client
from UnsavedChangesHandler import UnsavedChangesHandler
import Components.Client
from Host import Host

app = None

def main():
	global app
	
	
	# Arguments
	parser = argparse.ArgumentParser(description='A multi-process tab server.')
	parser.add_argument('-a','--add',type=int,default=0,help="the PID that this host will add immediately")
	args = parser.parse_args()
	arg_add = args.add
	
	print "Host PID",os.getpid()
	
	app = Host(arg_add)
	gtk.main()
	pass

if __name__ == "__main__":
	main()