#!/usr/bin/python

import ConfigParser

def get(attribute, default=None):
	return instance.get(attribute, default)

def get_bool(attribute, default=None):
	valid_true = 'yes sim on ligado true 1 y'.split(' ')
	return get(attribute, default) in valid_true

class Settings:
	loaded = False
	ini = ConfigParser.ConfigParser()
	def get(self, attribute, default=None):
		if (not self.loaded):
			self.load()
		if (self.ini.has_option('main', attribute)):
			return self.ini.get('main', attribute)
		else:
			return default

	def load(self):
		self.ini.read('config.ini')
		self.loaded = True

instance = Settings()

if __name__ == '__main__':
	testdata = ['playlists', 'playlist_prefix',
		'video_prefix', 'cache_path', 'fullscreen', 'outro']
	for attr in testdata:
		print attr, '=', repr(get(attr, 'xxxx'))
