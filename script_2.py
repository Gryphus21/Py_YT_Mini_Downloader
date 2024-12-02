import ddownr_api
from ddownr_api import VideoResolution
from ddownr_api import ProxyManager
from ddownr_api import DownloadStatus

import certifi
import ssl
import inspect

from pprint import pprint
import time
import logging
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.DEBUG, format="%(message)s")


client = ddownr_api.Client()

"""
response = client._request_video_download_on_server(media_url='', video_resolution=VideoResolution.MP4_720P)

pprint(f'_json_ob: {response._json_obj}')
print('\n\n')
print(f'success: {response.success}')
print(f'id: {response.id}')
print(f'content: {response.content}')
print(f'title: {response.title}')
print(f'info: {response.info}')
print(f'repeat_download: {response.repeat_download}')
print(f'message: {response.message}')
print(f'errors: {response.errors}')
print('\n\n')


while True:
    time.sleep(1)
    resp2 = client._get_download_progress(response)

    pprint(resp2._json_obj)
    print('\n\n')
    print(f'success: {resp2.success}')
    print(f'progress: {resp2.progress}')
    print(f'download_url: {resp2.download_url}')
    print(f'text: {resp2.text}')
    print(f'message: {resp2.message}')
    print('\n\n')

    if (resp2.success or resp2.download_url is None):
        print('Fine')
        break
"""


res: DownloadStatus = client.download_video_sync('', video_resolution=VideoResolution.MP4_1080P)

print(res)
print(f'info: {res.info}')
print(f'status: {res.status}')