#!/usr/bin/python

import logging
import socket
import urllib2
from time import time

TIMEOUT = 60.
socket.setdefaulttimeout(TIMEOUT)

def fetch(url, modified_since=None):
	return Fetcher(url, modified_since)

class Fetcher:
	def __init__(self, url, modified_since=None):
		self._resp = None
		self.date = modified_since
		self.status = 0
		logging.info('Requesting %s if modified since %s', url, modified_since)
		request = urllib2.Request(url)
		if modified_since != None:
			request.add_header('if-modified-since', modified_since)
		try:
			self._resp = response = urllib2.urlopen(request, None, TIMEOUT)
			self.date = response.info()['date']
			self.status = 200
			logging.debug('Server %s is new at %s',
				response.geturl(), self.date)
		except urllib2.HTTPError as err:
			logging.debug('Server says %s', err.getcode())
			self.status = err.getcode()

	def save(self, filename):
		next_smoke_sign = time() + 5.
		BUFSIZE = 512
		buffer = self._resp.read(BUFSIZE)
		logging.info('Storing at %s', filename)
		count = 0
		with open(filename, 'wb') as outfile:
			while len(buffer) > 0:
				outfile.write(buffer)
				count += len(buffer)
				if next_smoke_sign < time():
					logging.debug('Stored %d bytes so far', count)
					next_smoke_sign = time() + 5.
				buffer = self._resp.read(BUFSIZE)
		logging.debug('Stored %d bytes total', count)

if __name__ == '__main__':
	print 'nippl (c) 2010, Omar Balbuena'
	from sys import argv
	logging.basicConfig(level = logging.DEBUG)
	numargs = len(argv) - 1
	if 1 <= numargs <= 2:
		argv.pop(0) # remove app name
		if numargs < 2: argv.append(None)
		fetcher = Fetcher(*tuple(argv))
		if fetcher.status == 200:
			fetcher.save('testing-fetch.tmp')
	else:
		print 'Usage: [python] %s [ url [ date ]]' % argv[0]
		print 'Example: python %s http://www.python.org/' % argv[0], \
			"'Wed, 13 Apr 2011 21:58:57 GMT'"
