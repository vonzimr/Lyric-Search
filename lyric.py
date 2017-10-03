from tinytag import TinyTag
from bs4 import BeautifulSoup
import requests
import os

def search_ext(path, ext):
    matches = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("." + ext):
                matches.append(os.path.join(root, file))
    return matches




def lyric_wiki_search(q):
    search_url = "http://lyrics.wikia.com/wiki/Special:Search"
    payload = {'query': q}
    r = requests.get(search_url, params=payload)
    
    page = BeautifulSoup(r.text, 'html.parser')
    
    results = page.select(".result-link")
    for res in results:
        link = res.get('href')
        if ':' in link[7:]:
            print(link)
            lyrics = lyric_wiki_pull_lyrics(link)
            return lyrics

def replace_br(page):
    for br in page.find_all("br"):
        br.replace_with("\n")
    return page

def lyric_wiki_pull_lyrics(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    
    lyrics = replace_br(page.select('.lyricbox')[0]).get_text()
    return lyrics
    