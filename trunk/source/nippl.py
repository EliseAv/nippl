#!/usr/bin/python

import logging

from sync import Sync
from runner import Runner

if __name__ == '__main__':
	print 'nippl (c) 2010, Omar Balbuena'
	logging.basicConfig(level = logging.DEBUG)
	sync = Sync()
	runner = Runner()
	logging.info('Components are up!')
	playlist = sync.get_playlists()
	if len(playlist) > 0:
		runner.restart(playlist)
	while not runner.quit.is_set():
		if sync.refresh():
			playlist = sync.get_playlists()
			runner.restart(playlist)
		logging.info('Waiting %d minutes', sync.get_wait()/60)
		runner.quit.wait(sync.get_wait())
	print 'Quit.'