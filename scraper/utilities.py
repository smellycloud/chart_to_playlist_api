from bs4 import BeautifulSoup
import requests


def filter_tags(html_text):
    values = list()
    for value in html_text:
        values.append("\n".join([value.get_text(strip=True)]))
    return values

def extract_href(html_text):
    values = list()
    for value in html_text:
        values.append("\n".join([value.get_text(strip=True)]))
    return values

def extract_text(html_text):
    return "\n".join([html_text.get_text(strip=True)])

def clean_artist_name(name):
    stopwords = ['featuring', '&', ',', 'x', 'feat', 'feat.']
    name = name.split()
    result = [word for word in name if word.lower() not in stopwords]
    result = ' '.join(result)
    return result

class Soup:
    def __init__(self, url):
        self.url = url

    def get_soup(self):
        return BeautifulSoup(requests.get(self.url).text, 'html.parser')


def populate_billboard_countries():
    result = {}
    billboard_html = Soup('https://www.billboard.com/h/top-music-hits-world-international-song-charts/').get_soup()

    countries = billboard_html.find_all(attrs={}, name='strong')
    # print(filter_tags(countries))
    for country in countries:
        country = str(country)
        try:
            url = country.split('"')[1]
            country = country.split('">')[1].split('<')[0]
            key = country.replace(' ','_').lower()
            if 'Albums' not in country:
                result[key] = {'name': country, 'url': url}
        except:
            continue
    return result

# print(populate_billboard_countries())
