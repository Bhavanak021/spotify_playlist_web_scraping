from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/2000-08-12"

response = requests.get(URL)
raw_html = response.text
soup = BeautifulSoup(raw_html, 'html.parser')
song_list = []
songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
for song in songs:
    new_song = song.getText()
    song_list.append(new_song)


SPOTIPY_CLIENT_ID = "YOUR ID"
SPOTIPY_CLIENT_SECRET = "YOUR KEY"
SPOTIPY_REDIRECT_URI = "http://example.com"

#http://example.com/?code=AQCwVSEw1DScXj3mdObVjU0gJCi6QlQ4PbZppVzIk5dFw-hWLVu9lOs3dg5anf49PXyPL475rgU1kDM8KNxMK1GpqF0sX7Kyv8OeUv6rQ1T6NysBp5HAA1uxXel1ekLRkK2wx-GNdjAEGiP7ZgVHfAKRBtJsZF-u4iazuroMo-Gz7kdbfz3Ax0k1tK6LPQ4
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
date = input("What year you would like to travel to? Type in in YYYY-MM-DD format: ")
song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        # print(f"{song} doesn't exist in Spotify. Skipped.")
        pass

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)