import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

import requests
import re
from pytube import YouTube
from flask import Flask, render_template, request, send_file, Response

import zipfile

load_dotenv()

redirect_uri = "http://localhost:8000/callback"

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
download_path = os.getenv("DOWNLOAD_PATH")

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

app = Flask(__name__)

app_messages = []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        spotify_link = request.form["spotify_link"]
        if "track" in spotify_link:
            app_messages.clear()

            # Download the single song
            audio_data, audio_filename = download_song(spotify_link)
            return Response(
                audio_data,
                content_type="audio/mpeg",
                headers={
                    "Content-Disposition": f'attachment; filename="{audio_filename}"'
                },
            )
        elif "playlist" in spotify_link:
            app_messages.clear()

            # Download the playlist
            zip_filename = download_playlist(spotify_link)
            return send_file(zip_filename, as_attachment=True)
        else:
            return render_template("index.html", error="Invalid Spotify link.")
    return render_template("index.html", error=None, messages=app_messages)


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
    audio = yt.streams.filter(only_audio=True).first()
    audio_file_path = os.path.join(download_path, f"{yt.title}.mp3")
    audio.download(output_path=download_path, filename=f"{yt.title}.mp3")

    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()

    os.remove(audio_file_path)  # Remove the downloaded file from server

    return audio_data, f"{yt.title}.mp3"


def download_song(spotify_track_link):
    # Get track information
    song_name = get_track_info(spotify_track_link)
    app_messages.append(f"song name: {song_name}")
    print(song_name)

    # Search YouTube for the song
    yt_video_url = search_youtube(song_name)
    app_messages.append(f"youtube link: {yt_video_url}")
    print(yt_video_url)

    audio_data, audio_filename = download_audio(yt_video_url)
    app_messages.append("audio downloaded")
    return audio_data, audio_filename


def download_playlist(spotify_playlist_link):
    # Extract the playlist ID from the link
    playlist_id = spotify_playlist_link.split("/")[-1].split("?")[0]

    # Get the tracks from the playlist
    playlist_tracks = sp.playlist_tracks(playlist_id)

    audio_files = []

    for track in playlist_tracks["items"]:
        spotify_track_link = track["track"]["external_urls"]["spotify"]
        audio_data, audio_filename = download_song(spotify_track_link)
        audio_files.append((audio_data, audio_filename))

    zip_filename = "playlist.zip"

    with zipfile.ZipFile(zip_filename, "w") as playlist_zip:
        for audio_data, audio_filename in audio_files:
            playlist_zip.writestr(audio_filename, audio_data)

    return zip_filename


if __name__ == "__main__":
    app.run()
