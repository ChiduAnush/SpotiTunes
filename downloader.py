import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

redirect_uri = "http://localhost:8000/callback"

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

# Set up authentication
scope = "user-library-read"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
)

# ask user to enter the spotify link of the song.
spotify_track_link = input("Enter the Spotify song link: ")

# Extract the track ID from the link
track_id = spotify_track_link.split("/")[-1].split("?")[0]


# Get the track information
track_info = sp.track(track_id)
track_name = track_info["name"]
artist_name = track_info["artists"][0]["name"]
# track_url = track_info["preview_url"]

song_name = f"{artist_name} - {track_name}"
print(song_name)

# -----------------------

# https://www.youtube.com/results?search_query=

query = song_name.replace(" ", "+")
print(query)

yt_search_url = f"https://www.youtube.com/results?search_query={query}"
print(yt_search_url)
