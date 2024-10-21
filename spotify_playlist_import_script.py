
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import os
import time

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '47c68dfabfec4790a5efeaf3fbf29ed8'
SPOTIPY_CLIENT_SECRET = 'ee5127901ff84e06ba3c30a0f6678974'
SPOTIPY_REDIRECT_URI = 'http://localhost/'
SCOPE = 'playlist-modify-public'

# Authenticate with Spotify
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    ))
    user_id = sp.current_user()['id']
except Exception as e:
    print(f"Error during Spotify authentication: {e}")
    exit()

# Function to create a new playlist
def create_playlist(name, description):
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
    return playlist['id']

# Function to add tracks to the playlist
def add_tracks_to_playlist(playlist_id, tracks):
    track_uris = []
    for track in tracks:
        query = f"track:{track['name']} artist:{track['artist']}"
        print(f"Searching for track: {track['name']} by {track['artist']}")
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])
        time.sleep(0.5)  # Pause to prevent hitting rate limits
    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)

# Iterate through CSV files in the 'Playlists' folder
playlists_folder = r'C:\Users\manav\Desktop\Playlists'
for csv_file in os.listdir(playlists_folder):
    if csv_file.endswith('.csv'):
        playlist_name = os.path.splitext(csv_file)[0]
        playlist_description = f'A playlist imported from {csv_file}.'
        tracks = []
        
        # Read the CSV file and extract songs
        with open(os.path.join(playlists_folder, csv_file), newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tracks.append({'name': row['Song'], 'artist': row['Artist']})
        
        # Create a new playlist and add tracks
        playlist_id = create_playlist(playlist_name, playlist_description)
        add_tracks_to_playlist(playlist_id, tracks)
        
        print(f"Playlist '{playlist_name}' created and populated successfully!")
