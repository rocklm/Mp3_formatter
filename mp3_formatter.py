'''
===================================================================
Script: 
Mp3 Formatter

Purpose:
Ensure Artist and titles of a song are in the correct field

Notes:
(1) format of song string should be "<song title>" - "<artists>"

===================================================================
'''

#module import
from logging import getLogger
import os
import eyed3
import re

#supress CRC error from eyed3
getLogger().setLevel('ERROR')

#set music foled location
music_folder = 'C:\Entertainment\Music'

files = os.listdir(music_folder)

#'featuring' has a consistent naming convention
def feat_word_change(song_string):
    
    patterns = ['Ft.','ft.', 'Feat.', 'feat.', 'ft ', 'Ft', 'feat']
    for pattern in patterns:
        return song_string.replace(pattern, 'Feat')

#split title from artist and assign each to relevant field
def format_song(song_string):

    fix_feat = feat_word_change(song_string)

    split_string = fix_feat.split('-')
    if len(split_string) < 1:
        pass
    else:
        song = eyed3.load(music_folder + '\\' + song_string)
        song.tag.album_artist = split_string[0]
        song.tag.title = split_string[1]
        song.tag.save() 

#clean each song in file
def clean_songs():
    for song in files:
        format_song(song)

#call clean
if __name__ == '__main__':
    clean_songs()



