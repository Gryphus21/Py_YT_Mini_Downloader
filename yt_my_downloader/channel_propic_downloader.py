import urllib.request
from http.client import HTTPResponse

import json

import yt_my_downloader.http_utils as httputils
import my_custom_print.my_custom_print as mcp


def download_channel_propic(channel_url: str, destination_path: str, filename: str) -> bool:
    CONTENTFOREST_YTCD_XHR_URL = 'https://contentforest.com/api/tools/youtube-channel-data'
    REQUEST_HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/plain",
        #"Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "identity",
        "Content-Type": "application/json",
        #"Origin": "https://contentforest.com",
        #"DNT": "1",
        #"Alt-Used": "contentforest.com",
        #"Connection": "keep-alive",
        #"Referer": "https://contentforest.com/tools/youtube-pfp-downloader?url=",
        #"Sec-Fetch-Dest": "empty",
        #"Sec-Fetch-Mode": "cors",
        #"Sec-Fetch-Site": "same-origin",
        #"Sec-GPC": "1",
        #"TE": "trailers"
    }

    payload = {
        "youtube_channel_link": channel_url,
        "pick_keys": ["thumbnails"]
    }

    json_payload = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(url=CONTENTFOREST_YTCD_XHR_URL, method='POST', headers=REQUEST_HEADER, data=bytes(json_payload))
    response: HTTPResponse = urllib.request.urlopen(request)

    response_decoded = response.read().decode('utf-8')
    response_json = json.loads(response_decoded)

    if (len(response_json['thumbnails']) > 1):
        raise Exception('Più di una thumbnails è stata trovata, funzione non ancora implementata')
    
    #mcp.debug(f"URL: {channel_propic['url']}")
    #mcp.debug(f"width: {channel_propic['width']}")
    #mcp.debug(f"height: {channel_propic['height']}")

    return httputils.download_from_url(response_json['thumbnails'][0]['url'], destination_path, filename)