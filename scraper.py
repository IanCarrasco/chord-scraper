#%%
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import urllib
import billboard
from tqdm import tqdm
import pandas as pd
#%%
def get_chord_url(song):
    strRequest = song + " chords"

    strRequest = urllib.parse.quote_plus(strRequest)

    base_url = 'http://www.google.com/search?q=' + strRequest

    proxies = {'http': 'http://iansee:qweazsxdc@us-wa.proxymesh.com:31280',
               'https': 'http://iansee:qweazsxdc@us-wa.proxymesh.com:31280'}

    search_results = requests.get(base_url, proxies=proxies)

    soup = BeautifulSoup(search_results.text, "html.parser")

    print(soup)

    return soup.find('cite').text


def get_chords(songs):
    PROXY = "http://iansee:qweazsxdc@us-wa.proxymesh.com:31280" # IP:PORT or HOST:PORT
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--proxy-server=%s' % PROXY)


    #Initialize Headless Selenium Instance
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

    dataframe = []

    for idx, song in tqdm(enumerate(songs)):
        try:
            chord_url = get_chord_url(song[0].title)
            if chord_url:
                browser.get(chord_url)
                html = browser.page_source
                soup = BeautifulSoup(html)

                chords = []
                for match in soup.findAll('span', attrs={'class':'B24oE _1r_2U'}):
                    chords.append(match.string)
                
                if len(chords) > 0:
                    dataframe.append([song[0].artist, song[0].title, song[1], chords])

            if idx % 50 == 0:
                df = pd.DataFrame(dataframe, columns=["Artist", "Track", "Year", "Chords"])
                df.to_csv('./chords1.csv', index=False)
        except Exception as e:
            print(str(e))

    return df
#%%
def process_songs(chart, year):
    processed = []
    for song in chart:
        processed.append((song, year))
    return processed

songs = []
for year in tqdm(range(1950, 2020)):
    chart = billboard.ChartData('hot-100', date=str(year) + "-06-06")
    songs += process_songs(chart, year)

#%%

df = get_chords(songs)

#%%


#%%
