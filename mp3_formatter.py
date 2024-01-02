'''
===================================================================
Script: 
Mp3 Formatter

Purpose:
Ensure Artist and titles of a song are in the correct field

Notes:
(1) song name format  "<artists> Feat. <featured artists> - song title>"

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

#extract 
def find_string(pattern, string):
    try:
        txt = re.search(pattern, string).group(1)
    except:
        txt = ''
    return txt


#'featuring' has a consistent naming convention
def feat_word_change():
    
    patterns = ['Featuring', 'featuring', 'Ft ', 'ft ', 'FT', 'feat']
    files = os.listdir(music_folder)

    for song_name in files:
        old_song_path = music_folder + '\\' + song_name
    
        for pattern in patterns:
            new_song_path = old_song_path.replace(pattern, 'Feat.')
        
        os.rename(old_song_path, new_song_path)
            

#split title from artist and assign each to relevant field
def format_song(song_string):
    
    song = eyed3.load(music_folder + '\\' + song_string)
   
    #use original song title if no '-' which seperates the artist and title
    if '-' not in  song_string:
        song.tag.title = song_string.replace('.mp3', '')
    else:
       song.tag.title = find_string('\-(.*)', song_string).replace('.mp3', '')
     
    #use appropriate regex if song has featuring artists
    if 'Feat.' in song_string:
        main_artist_regex = '(.*)Feat\.'
    else:
        main_artist_regex = '(.*)\-' 
             
    song.tag.album_artist = find_string(main_artist_regex, song_string)
    song.tag.original_artist = find_string(main_artist_regex, song_string)
    #contributing artist
    song.tag.artist = find_string('Feat\.(.+?)\-', song_string)
  
    song.tag.save() 


#clean each song in file
def clean_songs():
    files = os.listdir(music_folder)
    for song_name in files:
        format_song(song_name)


#call clean
if __name__ == '__main__':
    feat_word_change() 
    clean_songs()