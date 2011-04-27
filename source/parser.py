#!/usr/bin/python

import data_objects
import fileinput

def parse(src_m3u):
	playlist = data_objects.Playlist()
	next_vid = data_objects.Video()
	for line in fileinput.FileInput(src_m3u):
		line = line.strip() # lines come with trailing newlines
		if len(line) == 0:
			pass # empty line, skip
		elif line[0] == '#':
			next_vid.add_attribute(line) # M3U attribute
		else:
			next_vid.set_filename(line) # found filename! done!
			playlist.append(next_vid)
			next_vid = data_objects.Video()
	return playlist

if __name__ == '__main__':
	newlist = parse('test.m3u')
	print newlist
	for i in newlist:
		print i
