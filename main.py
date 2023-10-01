import os

from pandas import read_csv
from dotenv import load_dotenv
from spotify import authentication
from fastapi import FastAPI
# from pydantic import BaseModel
from scraper.billboard import Billboard
from scraper.billboard_world import BillboardWorld
from spotify.utilities import Playlist
from scraper.utilities import populate_billboard_countries

# uvicorn main:app --reload

load_dotenv()
CONFIGURATION = {
    'SCOPE': 'playlist-modify-private user-top-read playlist-modify-public',
    'SPOTIPY_REDIRECT_URI': 'http://localhost:8080'
}

page_urls = {
    'billboardhot100': {'name': 'Billboard Hot 100',
                        'url': 'https://www.billboard.com/charts/hot-100/'},
    'billboard_tiktok': {'name': 'Billboard Tiktok',
                         'url': 'https://www.billboard.com/charts/tiktok-billboard-top-50/'},
    'billboard_streaming': {'name': 'Billboard Streaming',
                            'url': 'https://www.billboard.com/charts/streaming-songs/'},
    'billboard200_global': {'name': 'Billboard 200 Global',
                            'url': 'https://www.billboard.com/charts/billboard-global-200/'},
    'billboard_world': populate_billboard_countries(),
}
auth = authentication.Authenticate(client_id=os.getenv('CLIENT_ID'),
                                   client_secret=os.getenv('CLIENT_SECRET'))
current_user = auth(scope=CONFIGURATION['SCOPE'],
                    redirect_uri=CONFIGURATION['SPOTIPY_REDIRECT_URI'])
print(current_user.me())

app = FastAPI()


# class User(BaseModel):
#     name: str
#
#
# res = {
#     0: User(name=current_user.me()['display_name'])
# }


def run_pipeline(dataframe_name):
    if Playlist(user=current_user, dataframe_name=dataframe_name).create_spotify_playlist():
        return read_csv(os.path.join('data', dataframe_name + '.csv')).to_csv()
    else:
        return None


@app.get('/')
def index():
    return page_urls

@app.get('/{chart}')
def index(chart: str):
    return list(page_urls[chart].keys())


# ['billboardhot100', 'billboard_tiktok', 'billboard_streaming', 'billboard200_global', 'billboard_world']

@app.get('/{chart}/{date}')
def make_playlist(chart: str, date: str):
    return run_pipeline(dataframe_name=Billboard(date=date, chart=chart, page_urls=page_urls).get_tracks_dataframe())

@app.get('/{chart}/{country}/{date}')
def make_playlist(chart: str, country: str, date: str):
    print(chart, country, date)
    return run_pipeline(dataframe_name=BillboardWorld(date=date, chart=chart, page_urls=page_urls, country=country).get_tracks_dataframe())
