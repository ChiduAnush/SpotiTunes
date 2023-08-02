import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import re
from pytube import YouTube
import streamlit as st

# from dotenv import load_dotenv

# load_dotenv()

redirect_uri = "http://localhost:8000/callback"


# Function to get Spotify credentials from user input
def get_spotify_credentials():
    client_id = st.text_input("Spotify Client ID:")
    client_secret = st.text_input("Spotify Client Secret:", type="password")
    return client_id, client_secret


def setup_spotify_auth(client_id, client_secret):
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
    return sp


def get_download_path():
    path = st.text_input(
        "specify your folder path where you want to download your song(s) to:"
    )
    return path


def get_track_info(spotify_track_link):
    # Extract the track ID from the link
    track_id = spotify_track_link.split("/")[-1].split("?")[0]

    # Get the track information
    track_info = sp.track(track_id)
    track_name = track_info["name"]
    artist_name = track_info["artists"][0]["name"]
    song_name = f"{artist_name} - {track_name}"

    return song_name


def search_youtube(song_name):
    query = song_name.replace(" ", "+")
    yt_search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(yt_search_url)
    result_urls = re.findall(r"watch\?v=(\S{11})", response.text)
    yt_video_url = "https://www.youtube.com/watch?v=" + result_urls[0]

    return yt_video_url


def download_audio(yt_video_url, download_path):
    yt = YouTube(yt_video_url)
    audio = yt.streams.get_audio_only()
    audio.download(output_path=download_path, filename=f"{yt.title}.mp3")
    st.write("Downloaded audio")


def download_song(spotify_track_link):
    # Get track information
    song_name = get_track_info(spotify_track_link)
    st.write(song_name)

    # Search YouTube for the song
    yt_video_url = search_youtube(song_name)
    st.write(f"youtube link: {yt_video_url}")

    # Download the audio from YouTube
    download_audio(yt_video_url, download_path)


def download_playlist(spotify_playlist_link):
    # Extract the playlist ID from the link
    playlist_id = spotify_playlist_link.split("/")[-1].split("?")[0]

    # Get the tracks from the playlist
    playlist_tracks = sp.playlist_tracks(playlist_id)

    for track in playlist_tracks["items"]:
        # Get the Spotify track link
        spotify_track_link = track["track"]["external_urls"]["spotify"]

        # Download the song
        download_song(spotify_track_link)
    st.write("downloaded all songs, you can check your folder now ;)")


def main():
    st.title("Spotify Song Downloader")

    # Ask user for the spotify credentials
    client_id, client_secret = get_spotify_credentials()

    global download_path
    download_path = get_download_path()

    if download_path:
        if client_id and client_secret:
            # Setup Spotify authentication
            global sp
            sp = setup_spotify_auth(client_id, client_secret)

            spotify_link = st.text_input("Enter the Spotify link:")

            # Check if it's a single song or a playlist
            if "track" in spotify_link:
                # Download the single song
                if st.button("Download Single Song"):
                    download_song(spotify_link)
            elif "playlist" in spotify_link:
                # Download the playlist
                if st.button("Download Playlist"):
                    download_playlist(spotify_link)


if __name__ == "__main__":
    main()
