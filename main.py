import spotipy, os
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI='http://localhost:8080'
USERNAME = os.environ.get('USERNAME')
SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public" # request read/write access to your own private/public library and playlists
CACHE_PATH = ".cache-mark"

def get_playlist_id(playlists, name):
    """Return the playlist ID as a string."""
    for item in playlists['items']:
        if item['name'] == name: #Find specific playlist name from name param
            return item['id']

def get_song_uri(list_of_tracks):
    """Return a list of song URI/tracks from playlist dictionary."""
    tracks = []
    for item in list_of_tracks['items']:
        tracks.append(item['track']['uri'])
    return tracks

def refresh_token(sp_oauth):
    token_info = sp_oauth.get_cached_token()
    return sp_oauth.refresh_access_token(token_info["refresh_token"])

def main():
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, username=USERNAME, scope=SCOPE, cache_path=CACHE_PATH)
    token_info = refresh_token(sp_oauth) #Required since token expires every 60 minutes.
    sp = spotipy.Spotify(auth=token_info["access_token"])

    #Source playlist
    playlist_data = sp.current_user_playlists()
    id = get_playlist_id(playlist_data, name="Discover Weekly")
    song_info = []
    song_info = sp.playlist_tracks(id)
    song_uri_list = get_song_uri(song_info)

    #Destination playlist
    export_playlist_id = get_playlist_id(playlist_data, name="Discover Weekly Exports")
    export_song_info = []
    export_song_info = sp.playlist_tracks(export_playlist_id) 
    export_song_uri_list = get_song_uri(export_song_info)

    #Check if Discover Weekly song URI's already exist in destination playlist
    try:
        new_uri_list = []
        for uri in song_uri_list:
            if uri not in export_song_uri_list:
                new_uri_list.append(uri)
        sp.user_playlist_add_tracks(user=USERNAME, playlist_id=export_playlist_id, tracks=new_uri_list)
    except SpotifyException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()