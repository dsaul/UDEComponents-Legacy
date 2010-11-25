# See LICENCE for the source code licence.
# (c) 2010 Dan Saul

import sys,os,argparse
import gobject,pygtk,gtk
gobject.threads_init ()

from WebClient import WebClient

client = None

def main():
	global client
	
	# Arguments
	parser = argparse.ArgumentParser(description='A generic client example.')
	parser.add_argument('-o','--host',type=int,default=0,help="the PID that this client will embed itself into, if left out will spawn its own host")
	args = parser.parse_args()
	
	# DBus
	print "Client PID",os.getpid()
	
	client = WebClient(args.host)
	gtk.main()
	pass
	

	
if __name__ == "__main__":
	main()





































