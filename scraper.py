import requests, sys, json

#headers for GET request with client token
headers = {}
headers['Authorization'] = 'Bearer JKNNrVu4-koODkKVjcHJH1EmUA9I0mjkg8q-I57n3sXDfS5PJVZQf_F1ild_BPua'
headers['User-Agent'] = r'curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.'

def lyrics_url_by_id(id):
    songid = sys.argv[1]
    url = 'http://api.genius.com/songs/' + str(songid)
    response = requests.request('GET', url, headers=headers)

    if response.status_code != 200 :
        print ('Bad response from server: ' + response)
        sys.exit(-1);

    js = response.json()
    return (js['response']['song']['url'])


url = lyrics_url_by_id(sys.argv[1])
print (url)
