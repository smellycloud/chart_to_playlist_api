import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Authenticate:
    def __init__(self, client_id: object = None, client_secret: object = None):
        self.client_id = client_id
        self.client_secret = client_secret

    def __call__(self, scope=None, redirect_uri=None):
        return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                         client_id=self.client_id,
                                                         redirect_uri=redirect_uri,
                                                         client_secret=self.client_secret))