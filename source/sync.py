#!/usr/bin/python

import copy
import cPickle
import logging
import os
import subprocess
from time import time

from fetcher import fetch
from parser import parse
import settings

class SyncStamps:
	def __init__(self, videos={}, playlists={}, expires=0.0):
		self.videos = videos
		self.playlists = playlists
		self.expires = expires

class Sync:
	def __init__(self):
		self._playlist_prefix = settings.get('playlist_prefix')
		self._video_prefix = settings.get('video_prefix')
		self.playlists = settings.get('playlists').split(',')
		self._cache_path = settings.get('cache_path')
		self._make_dirs('current')
		self.stamps = self._make_stamps('current')
		logging.info('Instantiated sync manager')

	def _path(self, *items):
		return os.path.join(self._cache_path, *items)

	def _nuke_path(self, *where):
		subprocess.call(['rm', '-rf', self._path(*where)])

	def _make_stamps(self, state, original=None):
		stamps_path = self._path(state, 'stamps.pickle')
		if os.path.exists(stamps_path):
			with open(stamps_path, 'rb') as f:
				return cPickle.load(f)
		elif original is None:
			return SyncStamps()
		else:
			return copy.deepcopy(original)

	def _make_dirs(self, dir):
		fullpath = self._path(dir)
		if not os.path.exists(fullpath):
			os.makedirs(fullpath, 0755)

	def refresh(self, force=False):
		if time() < self.stamps.expires and not force:
			logging.info('Current files good for %.1f more secs', self.get_wait())
			return False

		self._nuke_path('new')
		self._make_dirs('new')
		new_stamps = self._make_stamps('new', self.stamps)
		changed = False

		available = set()
		for playlist in self.playlists:
			changed |= self._refresh_playlist(playlist, new_stamps, available)

		for video in self._find_videos(available):
			changed |= self._refresh_video(video, new_stamps, set())

		new_stamps.expires = time() + (float(settings.get('refresh_hours')) * 3600)

		if changed:
			self._swap_into_new()
		else:
			self._nuke_path('new')
		self.stamps = new_stamps
		self._save_stamps('current', new_stamps)
		return changed

	def _refresh_playlist(self, playlist, stamps, available):
		try: return self._refresh(self._playlist_prefix,
			playlist, stamps.playlists, available)
		finally: self._save_stamps('new', stamps)

	def _refresh_video(self, video, stamps, available):
		try: return self._refresh(self._video_prefix,
			video, stamps.videos, available)
		finally: self._save_stamps('new', stamps)

	def _refresh(self, url_prefix, item, stamps_dict, available):
		try:
			known_item = item in stamps_dict
			stamp = None
			if known_item and os.access(self._path('current', item), os.R_OK):
				stamp = stamps_dict[item]
			resp = fetch(url_prefix + item, stamp)
			local_path = self._path('new', item)

			if resp.status >= 400: # error statuses
				if known_item:
					del stamps_dict[item]
				return known_item # changed if previously known

			elif resp.status == 304: # not modified
				available.add(item)
				os.link(
					self._path('current', item),
					self._path('new',     item))
				stamps_dict[item] = resp.date
				return False # unchanged

			elif 200 <= resp.status < 300: # downloading
				available.add(item)
				resp.save(local_path)
				stamps_dict[item] = resp.date
				return True # changed

			else:
				raise Exception("Don't know what to do with response %s", resp.status)

		except:
			import traceback
			logging.error('Failed to fetch %s%s. Skipping. Exception info:\n%s',
				url_prefix, item, traceback.format_exc())
			return False # assume unchanged

	def _save_stamps(self, folder, stamps):
		with open(self._path(folder, 'stamps.pickle'), 'wb') as f:
			cPickle.dump(stamps, f, 0)

	def _find_videos(self, playlists):
		videos = set()
		for filename in playlists:
			playlist = parse(self._path('new', filename))
			for video in playlist:
				videos.add(str(video))
		return videos

	def _swap_into_new(self):
		if os.access(self._path('current'), os.W_OK):
			os.rename(self._path('current'), self._path('old'))
		os.rename(self._path('new'), self._path('current'))
		if os.access(self._path('old'), os.W_OK):
			self._nuke_path('old')
			
	def get_playlists(self):
		result = []
		for playlist in self.stamps.playlists:
			result.append(self._path('current', playlist))
		return result
		
	def get_wait(self):
		return max(0, self.stamps.expires - time())

if __name__ == '__main__':
	print 'nippl (c) 2010, Omar Balbuena'
	logging.basicConfig(level = logging.DEBUG)
	sync = Sync()
	sync.refresh(True)
