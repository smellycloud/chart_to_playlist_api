import scraper.utilities
from pandas import DataFrame
import os


class Billboard:
    def __init__(self, date, chart, page_urls):
        self.date = date
        self.chart = chart
        self.page_urls = page_urls

    title_class = ('c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet '
                   'lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis '
                   'u-max-width-330 u-max-width-230@tablet-only')
    artist_class = ('c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max '
                    'u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block '
                    'a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only')

    def get_tracks_dataframe(self):
        dataframe_path = os.path.join(os.path.dirname(__file__), '..', 'data',
                                      self.page_urls[self.chart]['name'] + ' ' + self.date + '.csv')
        if os.path.isfile(dataframe_path):
            print('Billboard::get_tracks_dataframe: .csv file exists')
            return self.page_urls[self.chart]['name'] + ' ' + self.date

        track_titles = list()
        track_artists = list()

        billboard_html = scraper.utilities.Soup(self.page_urls[self.chart]['url'] + self.date).get_soup()

        first_title = billboard_html.find_all(attrs={
            'class': 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet '
                     'lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis '
                     'u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet'
        }, name='h3')
        if first_title is []:
            return None

        track_titles.append(scraper.utilities.filter_tags(html_text=first_title))

        first_artist = billboard_html.find_all(attrs={
            'class': 'c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max '
                     'u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block '
                     'a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet'
        }, name='span')
        track_artists.append(scraper.utilities.filter_tags(html_text=first_artist))

        titles = billboard_html.find_all(attrs={
            'class': self.title_class,
        }, name='h3')
        track_titles.append(scraper.utilities.filter_tags(html_text=titles))

        artists = billboard_html.find_all(attrs={
            'class': self.artist_class,
        }, name='span')
        track_artists.append(scraper.utilities.filter_tags(html_text=artists))

        track_titles = [item for sublist in track_titles for item in sublist]
        track_artists = [item for sublist in track_artists for item in sublist]

        track_df = DataFrame({
            'track': track_titles,
            'artist': track_artists
        })

        track_df.to_csv(os.path.abspath(dataframe_path))
        return self.page_urls[self.chart]['name'] + ' ' + self.date
