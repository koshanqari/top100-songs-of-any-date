from concurrent.futures import process
import encodings
from operator import index
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint




date = "2000-08-12"
date = input("Top songs of which date do you want to play ?(yyyy-mm-dd)")
#------------------------
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
print(response)

soup = BeautifulSoup(response.text, "html.parser")
label = soup.select(selector="h3#title-of-a-story.c-title.a-no-trucate.a-font-primary-bold-s.u-letter-spacing-0021")


songs_list = [item.string for item in label]
songs_list = [item.replace("\n", "", 2) for item in songs_list]
#------------------

#create 2 environmental Variables ------------------>>>

# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
#use $En:<variable-name>=<varible value> in vs code  

# or add these besides score=scope,
#client_id="a0df39b5****************************"
#client_secret='9a0367***************************'

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri="http://example.com" ))
print(sp.current_user()['id'])
user_id = sp.current_user()['id']




uri_list = []
for song in songs_list:
    print(songs_list.index(song), song,date.split("-")[0])
    result = sp.search(q=f'track:{song} year:{date.split("-")[0]}', type='track')
    try:
        uri_list.append(result['tracks']["items"][0]["uri"])
    except:
        print("not found, skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{date}'s Top 100", public=False)

input("Above songs have been added. Press any key to continue:")

print("\n\n--------------\n\n")

sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list, position=None)