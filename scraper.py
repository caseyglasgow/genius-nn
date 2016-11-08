import requests, sys, json, re, os
from bs4 import BeautifulSoup
from urllib.parse import quote

#headers for GET request with client token
headers = {}
headers['Authorization'] = 'Bearer JKNNrVu4-koODkKVjcHJH1EmUA9I0mjkg8q-I57n3sXDfS5PJVZQf_F1ild_BPua'
headers['User-Agent'] = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'

def api_js(url):
    response = requests.request('GET', url, headers=headers)
    if response.status_code != 200 :
        print ('Bad response from server: ' + response)
        sys.exit(-1);
    js = response.json()
    return js

def lyrics_url_by_id(id):
    songid = sys.argv[1]
    url = 'http://api.genius.com/songs/' + str(songid)
    res = api_js(url)
    return (res['response']['song']['url'])

def get_lyric_text(url):
    req = requests.get(url)
    lyricsoup = BeautifulSoup(req.content, "lxml")
    lyricdata = lyricsoup.find('lyrics').get_text()
    lyricdata.replace('\n',' ')
    return lyricdata

# get the api path to the artist of the first song returned by the search to
# the given keyword (most likely a song)
def artist_path_by_search(search):
    url = r'http://api.genius.com/search?q=' + quote(search)
    js = api_js(url)
    results = js['response']['hits']

    print ('First results is a: ' + results[0]['type'])

    first = results[0]['result']
    api_path = first['api_path']
    print('Title: ' + first['full_title'])
    url = r'http://api.genius.com' + api_path
    song_js = api_js(url)
    artist_path = song_js['response']['song']['primary_artist']['api_path']
    #js = api_js(r'http://api.genius.com' + artist_path)
    #artist_string = js['response']['artist']['alternate_names']
    #print ('Artist name(s): ' + artist_string[0])
    return artist_path

def get_song_url_list(path, filename, maxpg=100):
    song_url_list = []
    page = 1
    perpage = 20
    nextpage = 1
    song_list_file = open(filename + '.list', 'w')
    while (nextpage is not None) and ( page <= maxpg):
        print('Searching page ' +str(page))

        url = r'http://api.genius.com' + path + '/songs?per_page='+str(perpage)+'&page='+str(page)
        js = api_js(url)
        nextpage = js['response']['next_page']
        page += 1
        songs = js['response']['songs']
        for song in songs:
            song_url_list.append(song['url'])
            song_list_file.write(song['title'])
        pass
    song_list_file.close()
    print('Found ' + str(len(song_url_list)) + ' songs')
    return song_url_list

def write_lyrics_file(url_list, filename):
    out = open(filename, 'w')
    count = 0
    for url in url_list:
        text = get_lyric_text(url)
        out.write(text)
        count +=1
        if count % 25 == 0:
            print('Written ' + str(count) + ' songs')
    out.close()



def main():
    if len(sys.argv) < 3:
        print('usage: ' + sys.argv[0] + 'search_string output_file [max_pages]')
    if(len(sys.argv) == 4):
        max_pages = sys.argv[3]

    artist_path = artist_path_by_search(sys.argv[1])
    song_urls = get_song_url_list(artist_path,int(max_pages))

    write_lyrics_file(song_urls, sys.argv[2])



if __name__ == '__main__':
    main()
