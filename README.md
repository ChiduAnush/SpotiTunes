# Spotify Downloader

A simple python script to download individual songs, or whole playlists, from spotify.

### Prerequisites

- python3.x
- dependencies (install using `pip install -r requirements.txt`):
  - spotipy
  - dotenv
  - requests
  - re
  - pytube

## Getting Started

1. spotify developer account (https://developer.spotify.com/dashboard)

- create an app
- keep the client ID, and client Secret handy.

2. Clone this repository.

3. pip install the dependencies (refer the prerequisites)

4. set the variables in the `.env` file.

   - just open the `.env.example` file in the repo, set the variables.
   - then rename the file from `.env.example` to `.env`.

5. Done! Run the script by,
   - `python3 downloader.py`
