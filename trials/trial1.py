# THIS IS TRIAL CODE, JUST FOR UNDERSTANDING.
# The final working code is downloader.py


import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

import requests
import re

from pytube import YouTube


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

query = song_name.replace(" ", "+")
# print(query)

# make the url for the youtube search with the query
yt_search_url = f"https://www.youtube.com/results?search_query={query}"

# get html response from the yt_search_url
response = requests.get(yt_search_url)

# get all results with the matching pattern, from the html response
result_urls = re.findall(r"watch\?v=(\S{11})", response.text)

# getting only the first search result, and appending it to the basic youtube search url
yt_video_url = "https://www.youtube.com/watch?v=" + result_urls[0]

print(yt_video_url)

# ----------------------------

# create a youtube object
yt = YouTube(yt_video_url)
print("youtube video title: ", yt.title)

# get the audio from the url.
audio = yt.streams.get_audio_only()

# download the audio to your desired path
audio.download(output_path="/Users/chiduanush/Desktop", filename=f"{yt.title}.mp3")

print("downloaded video")
