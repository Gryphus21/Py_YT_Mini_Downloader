import os

from colorama import init as colorama_init

import ddownr_api
from ddownr_api import VideoResolution
import my_custom_print.my_custom_print as mcp

colorama_init()

c = ddownr_api.Client()
#c.download_video_sync('https://www.youtube.com/watch?v=9JWkiltjRfQ', VideoResolution.MP4_720P)
c.download_video_sync('https://www.youtube.com/shorts/vQbyMPX79sY', video_resolution=VideoResolution.MP4_720P)
