import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.request
import os

# ask user to enter the client id and client secret
client_id = input("Enter your client ID: ")
client_secret = input("Enter your client secret: ")
redirect_uri = "http://localhost:8000/callback"

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

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
)


# Prompt the user for the Spotify track link
spotify_track_link = input("Enter the Spotify track link: ")

# # Extract the track ID from the link
# track_id = spotify_track_link.split("/")[-1]

# Extract the track ID from the link
track_id = spotify_track_link.split("/")[-1].split("?")[0]


# Get the track information
track_info = sp.track(track_id)
track_name = track_info["name"]
artist_name = track_info["artists"][0]["name"]
track_url = track_info["preview_url"]

# Download the track
if track_url:
    file_name = f"{artist_name} - {track_name}.mp3"
    file_path = f"/Users/chiduanush/Desktop/{file_name}"  # Replace with your desired folder path
    urllib.request.urlretrieve(track_url, file_path)
    print(f"Downloaded: {file_name}")
else:
    print(f"No preview available for: {track_name}")
