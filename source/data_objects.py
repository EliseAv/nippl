#!/usr/bin/python

class Playlist(list):
	def export(self, filename):
		with open(filename, 'w') as f:
			for v in self:
				f.writelines([str(v), '\n'])

class Video:
	def __init__(self):
		self.filename = None
	def __str__(self):
		return self.filename
	def set_filename(self, name):
		# discard folder information, only use filename
		position = reduce(max, map(name.rfind, '/\\'))
		self.filename = name[position + 1 :]
	def add_attribute(self, attribute):
		pass # not implemented, and i don't see a reason to
