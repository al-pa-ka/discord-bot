from pytube import *
import operator
from youtube_search import *


def get_url(url: str):

    vid_info = YouTube(url=url).vid_info

    formats = vid_info['streamingData']['adaptiveFormats']

    needed_formats = []

    for format1 in formats:
        if format1['mimeType'].endswith('"opus"'):
            needed_formats.append(format1)

    needed_formats.sort(key=operator.itemgetter('bitrate'))

    url = needed_formats[-1]['url']

    return url


def get_download(url):
    yt_object = YouTube(url)
    formats = yt_object.vid_info['streamingData']['adaptiveFormats']
    needed_formats = []

    for _format in formats:
        if str(_format['mimeType']).startswith('audio/mp4'):
            needed_formats.append(_format)

    needed_formats.sort(key=operator.itemgetter('bitrate'), reverse=True)
    url = needed_formats[0]['url']

    return url


def get_list_(name: str):
    results = YoutubeSearch(name, max_results=10).to_dict()

    videos = []
    for result in results:

        url = 'https://www.youtube.com' + result['url_suffix'] + result['id']
        title = result['title']
        channel = result['channel']

        videos.append({'url': url, 'title': title, 'channel': channel})

    return videos


def get_info(url: str):
    yt = YouTube(url=url)
    info = yt.vid_info
    thumbnail = info['videoDetails']['thumbnail']['thumbnails'][1]['url']
    title = info['videoDetails']['title']
    author = info['videoDetails']['author']
    return title, author, thumbnail

