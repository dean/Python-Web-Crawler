from httplib import *
from threading import Timer
import urlparse
import urllib
import urllib2
import socket
import os.path

def get_link(inp):
	found = inp.find("http://")
	if inp.find("https://")>=0:
		found = inp.find("https://")
	if found>=0:
		end = inp.find(" ", found)
		inp = inp[found:end]
		if inp.find("\"")>= 0:
			end = inp.find("\"")
			return inp[:end]
		return inp
	else:
		return -1 ## If a link is not found in the current string

def collect_links(data):
	links = []
	i = 0
	for line in data.split("\n"):
		i+=1
		if i%50==0:
			print i	
		link = get_link(line)
		if link != -1:
			links.append(link+"\n")
	return links	

def goto_link(link):
	try:
		con = urllib.urlopen(link)
		socket.setdefaulttimeout(2)
	except IOError, socket.timeout:
		print "Socket timeout: ", link
		return
	t = Timer(2.0, con.close)
	t.start()
	FILE = open(filename, "a")

	print "Webpage ", link, "was found!"
	try:
		links = collect_links(con.read())
		t.cancel()
	except TypeError:
		print "Timeout on ", link
		return
	con.close();
	FILE.writelines(links)
	for l in links:
		print "Going to link ", l
		goto_link(l)

filename = "webLinks.txt"
if os.path.exists(filename):
	FILE = open(filename, "a")
	FILE.write("")
	FILE.close()
else:
	FILE = open(filename, "w")
	FILE.write("")
	FILE.close()

#goto_link("wikipedia.org/wiki/Gadsden_flag")
goto_link("http://www.google.com")
FILE.close()
