#!/usr/bin/python

import os
import subprocess
import settings
import threading

os_call_list = {
	'Linux': '/usr/bin/cvlc',
	'Darwin': '/Applications/VLC.app/Contents/MacOS/VLC'}

class Runner:
	def __init__(self):
		platform = os.uname()[0]
		self.invocation = [
			os_call_list[platform],
			'--loop',
			'--no-video-title-show',
			'--play-and-exit']
		if settings.get_bool('fullscreen', True):
			self.invocation.append('--fullscreen')
		self.proc = None
		self.quit = threading.Event()
		self.restart_lock = threading.Lock()
		self._harakiri = threading.Event()
		thread = threading.Thread(target=self._poll)
		thread.daemon = True
		thread.start()
	def restart(self, playlists):
		with self.restart_lock:
			self._ensure_not_running()
			self.proc = subprocess.Popen(self.invocation + playlists)
	def _poll(self):
		while not self._harakiri.wait(1):
			with self.restart_lock:
				if self.proc == None or self.proc.poll() != None:
					self.quit.set()
				else:
					self.quit.clear()
	def __del__(self):
		self._harakiri.set()
		self._ensure_not_running()
	def _ensure_not_running(self):
		if self.proc != None:
			self.proc.terminate()
			self.proc.wait()

if __name__ == '__main__':
	import parser
	import time
	playlist = parser.parse('test.m3u')
	filename = 'local.m3u'
	playlist.export(filename)
	runner = Runner(filename)
	time.sleep(10)
	print "10 seconds passed, restarting"
	runner.restart()
	time.sleep(10)
	print "10 more seconds gone, quitting"
	del runner
