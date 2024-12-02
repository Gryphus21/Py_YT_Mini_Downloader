__version__ = 'Alpha-1'
__author__ = 'Gryphus21'

from ddownr_api.client import Client
from urllib3 import ProxyManager

from ddownr_api.response_status import DownloadProgressResponse
from ddownr_api.response_status import RequestVideoDownloadResponse
from ddownr_api.response_status import DownloadStatus

from ddownr_api.video import VideoResolution