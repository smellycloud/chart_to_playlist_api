import numpy as np
import pandas as pd
import os
import scraper.utilities
import progressbar


class Search:
    def __init__(self, user=None, track_name=None, artist=None):
        self.user = user
        self.track_name = track_name
        self.artist = scraper.utilities.clean_artist_name(artist)
        self.track_info = self.user.search(q='artist:' + self.artist + ' track:' + self.track_name, type='track',
                                           limit=10, offset=0, market=None)

    def get_track_id(self):
        try:
            result = str(self.track_info['tracks']['items'][0]['id'])
            return result if len(result) > 0 else np.nan
        except:
            return np.nan

    def get_track_popularity(self):
        try:
            result = str(self.track_info['tracks']['items'][0]['popularity'])
            return result if len(result) > 0 else np.nan
        except:
            return np.nan

    def get_track_preview_url(self):
        try:
            result = str(self.track_info['tracks']['items'][0]['preview_url'])
            return result if len(result) > 0 else np.nan
        except:
            return np.nan

    def get_track_duration(self):
        try:
            result = str(self.track_info['tracks']['items'][0]['duration_ms'])
            return result if len(result) > 0 else np.nan
        except:
            return np.nan

    def get_release_date(self):
        try:
            result = str(self.track_info['tracks']['items'][0]['album']['release_date'])
            return result if len(result) > 0 else np.nan
        except:
            return np.nan

    def get_artwork_url(self):
        try:
            result = str(self.track_info['tracks']['items'][0]['album']['images'][0]['url'])
            return result if len(result) > 0 else np.nan
        except:
            return np.nan


class Playlist:
    def __init__(self, user=None, dataframe_name=None, api_batch_size=100):
        self.user = user
        self.dataframe_name = dataframe_name
        self.dataframe_path = os.path.join(os.path.dirname(__file__),
                                           '..',
                                           'data',
                                           self.dataframe_name + '.csv')
        self.api_batch_size = api_batch_size

    widgets = [' [',
               progressbar.Timer(format='Progress:'),
               '] ',
               progressbar.Bar('*'),
               ]

    def append_track_info_to_df(self):
        if self.dataframe_name is None or self.dataframe_name == '':
            return None
        else:
            try:
                return pd.read_csv(os.path.abspath(self.dataframe_path))['id']
            except:
                dataframe = pd.read_csv(os.path.abspath(self.dataframe_path))
                track_ids = list()
                track_popularity = list()
                track_preview_url = list()
                track_duration = list()
                release_date = list()
                artwork_url = list()

                bar = progressbar.ProgressBar(max_value=len(dataframe), widgets=self.widgets)

                for i, row in dataframe.iterrows():
                    track = Search(user=self.user, track_name=row['track'], artist=row['artist'])
                    track_id = track.get_track_id()
                    if track_id is not np.nan or len(str(track_id)) > 0:
                        track_ids.append(track_id)
                        track_popularity.append(track.get_track_popularity())
                        track_preview_url.append(track.get_track_preview_url())
                        track_duration.append(track.get_track_duration())
                        release_date.append(track.get_release_date())
                        artwork_url.append(track.get_artwork_url())
                    else:
                        track_ids.append(np.nan)
                        track_popularity.append(np.nan)
                        track_preview_url.append(np.nan)
                        track_duration.append(np.nan)
                        release_date.append(np.nan)
                        artwork_url.append(np.nan)
                    bar.update(int(i))
                dataframe['id'] = track_ids
                dataframe['popularity'] = track_popularity
                dataframe['preview_url'] = track_preview_url
                dataframe['duration'] = track_duration
                dataframe['release_date'] = release_date
                dataframe['artwork_url'] = artwork_url
                dataframe.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                              '..',
                                                              'data',
                                                              self.dataframe_name + '.csv')))
                return track_ids


    def create_spotify_playlist(self):
        if self.dataframe_name is None or self.dataframe_name == '':
            return False
        track_ids = self.append_track_info_to_df()
        track_ids = [track for track in track_ids if str(track) != str(np.nan)]
        try:
            playlist = self.user.user_playlist_create(user=self.user.me()['id'],
                                                      name=self.dataframe_name,
                                                      public=False,
                                                      collaborative=False)
            print(self.dataframe_name)
            # spotify only allows 100 tracks per request :(. splitting playlist into batches instead.
            while True:
                if len(track_ids) > self.api_batch_size:
                    batch = track_ids[:self.api_batch_size]
                    track_ids = track_ids[self.api_batch_size:]
                else:
                    self.user.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
                    break
                self.user.playlist_add_items(playlist_id=playlist['id'], items=batch)
            print('(spotify) utilities::create_spotify_playlist: success')
            return True
        except:
            print('(spotify) utilities::create_spotify_playlist: could not create playlist')
            return False
        finally:
            print('(spotify) utilities::create_spotify_playlist: run complete')
