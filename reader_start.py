from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import os
import getpass

import sys

def get_url_content(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """ Wenn url eine HTML ist, wird True zurückgegeben """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def get_playlist_title(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')
    playlist_title_tag = html.find("meta", property="og:title")
    return playlist_title_tag["content"] if playlist_title_tag else "No meta title given"
    playlist_title = ""
    for title in html.select('meta'):
        if title == ['title']:
            playlist_title = title.text
            playlist_title = playlist_title.strip()
    return playlist_title

def get_music_titles(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')

    contents = html.find("span", id="video-title")
    print(contents.text)

    music_title = []
    for row in html.select('tr'):
        music_title.append(row['data-title'])
    return music_title

def input_path():
    print("File-Path: (When no input -> C:/PlaylistDatas)")
    file_path = input() + "\\"
    if file_path == "\\":
        username = getpass.getuser()
        try:
            os.mkdir("C:/PlaylistDatas")
            file_path = "C:/PlaylistDatas/"
        except:
            file_path = "C:/PlaylistDatas/"
    return file_path

def write_file(file_path, playlist_title, music_title):
    new_file = file_path + playlist_title + ".txt"
    file = open(new_file, "w", encoding="utf-8")
    for title in music_title:
        file.write(title + "\n")
    file.close()

print("YouTube-Playlist URL: (write any character before URL, otherwise URL will be opened in Browser)")
web_url = input()
file_path = input_path()
web_url = web_url[1:]
raw_html = get_url_content(web_url)
write_file(file_path, get_playlist_title(raw_html), get_music_titles(raw_html))