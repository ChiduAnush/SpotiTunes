import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import re
from pytube import YouTube
import streamlit as st
from io import BytesIO

# from dotenv import load_dotenv

# load_dotenv()

redirect_uri = spotipy.oauth2.SpotifyOAuth.REDIRECT_URI


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


def download_audio(yt_video_url):
    yt = YouTube(yt_video_url)
    audio_stream = yt.streams.get_audio_only()

    # Download the audio as bytes
    with BytesIO() as buffer:
        audio_stream.stream_to_buffer(buffer)
        audio_bytes = buffer.getvalue()

    return audio_bytes, yt.title


def download_song(spotify_track_link):
    # Get track information
    song_name = get_track_info(spotify_track_link)
    st.write(song_name)

    # Search YouTube for the song
    yt_video_url = search_youtube(song_name)
    st.write(f"youtube link: {yt_video_url}")

    audio_bytes, yt_title = download_audio(yt_video_url)

    st.download_button(
        label="Download MP3", data=audio_bytes, file_name=f"{yt_title}.mp3"
    )


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


# def main():
st.title("Spotify Song Downloader")


# Initialize the Spotify API client with your credentials
client_id = st.secrets["CLIENT_ID"]
client_secret = st.secrets["CLIENT_SECRET"]
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-library-read",
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
)


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


# if __name__ == "__main__":
#     main()