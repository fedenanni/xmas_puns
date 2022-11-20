from lyricsgenius import Genius
import pandas
import json
import configparser
import re

# Get configuration file
config = configparser.ConfigParser()
config.sections()
config.read('../config/api.ini')
token = config.get('main', 'secret')

genius = Genius(token)

df = pandas.read_csv("data/top100.csv")
data = []

for idx,row in df.iterrows():
    title = row["Title"].replace('"', '')
    artist = row["Artist"]
    try:
        song = genius.search_song(title, artist)
        print(song)
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
        
    except Exception as e:
        print(e)

with open('data/data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)