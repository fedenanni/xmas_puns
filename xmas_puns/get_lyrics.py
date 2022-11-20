from lyricsgenius import Genius
import pandas
import time
import json
import os
import configparser
import re

# Get configuration file
config = configparser.ConfigParser()
config.sections()
config.read('../config/api.ini')
token = config.get('main', 'secret')

genius = Genius(token)

df = pandas.read_csv("data/top100.csv")[:5]
data = []

for idx,row in df.iterrows():
    title = row["Title"].replace('"', '')
    artist = row["Artist"]
    try:
        song = genius.search_song(title)
        
        clean_lyrics = song.lyrics.split("Lyrics")[1]
        clean_lyrics = clean_lyrics.split("Embed")[0]
        clean_lyrics = "".join(re.split("\(|\)|\[|\]", clean_lyrics)[::2])

        data.append(
            {
                'artist':song.artist,
                'title':title,
                'lyrics':clean_lyrics
            }
        )
        #time.sleep(.30)
        
    except Exception as e:
        print(e)

with open('data/data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)