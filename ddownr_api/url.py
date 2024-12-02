from ddownr_api.video import VideoResolution

class TOKEN():
    API = 'dfcb6d76f2f6a9894gjkege8a4ab232222'

class COPYRIGHT():
    NO = '0'
    YES = '1'

class BASE_URL():
    URL = 'p.oceansaver.in'

class URL_PATH():
    DOWNLOAD_URL_PATH = '/ajax/download.php'
    PROGRESS_URL_PATH = '/ajax/progress.php'

class DOWNLOAD_URL_FIELDS():
    COPYRIGHT = 'copyright'
    FORMAT = 'format'
    URL = 'url'
    API = 'api'

class PROGRESS_URL_FIELDS():
    ID = 'id'


class XHR_URL():
    #NOTE: Oldests
    #DOWNLOAD = '{}p.oceansaver.in/ajax/download.php?copyright={}&format={}&url={}&api={}'
    #PROGRESS = '{}p.oceansaver.in/ajax/progress.php?id={}'

    DOWNLOAD_URL = '{}' + BASE_URL.URL + URL_PATH.DOWNLOAD_URL_PATH
    PROGRESS_URL = '{}' + BASE_URL.URL + URL_PATH.PROGRESS_URL_PATH

class UrlMaker():
    @staticmethod
    def _protocol(use_https: bool):
        return 'https://' if use_https else 'http://'

    @DeprecationWarning
    @staticmethod
    def make_download_url(media_url: str, video_resolution: VideoResolution, use_https: bool, api_token: str = TOKEN.API, copyright: str = COPYRIGHT.NO) -> str:
        return XHR_URL.DOWNLOAD.format(UrlMaker._protocol(use_https), copyright, video_resolution.url_format, media_url, api_token)

    @DeprecationWarning
    @staticmethod
    def make_progress_url(media_id: str, use_https: bool) -> str:
        return XHR_URL.PROGRESS.format(UrlMaker._protocol(use_https), media_id)
    


    @staticmethod
    def get_download_url(use_https: bool) -> str:
        return XHR_URL.DOWNLOAD_URL.format(UrlMaker._protocol(use_https))
    
    @staticmethod
    def get_progress_url(use_https: bool) -> str:
        return XHR_URL.PROGRESS_URL.format(UrlMaker._protocol(use_https))
    
    @staticmethod
    def get_download_url_fields(media_url: str, video_resolution: VideoResolution, api_token: str = TOKEN.API, copyright: str = COPYRIGHT.NO) -> dict:
        return {DOWNLOAD_URL_FIELDS.COPYRIGHT : copyright,
                DOWNLOAD_URL_FIELDS.FORMAT : video_resolution.url_format,
                DOWNLOAD_URL_FIELDS.URL : media_url,
                DOWNLOAD_URL_FIELDS.API : api_token}

    @staticmethod
    def get_progress_url_fields(media_id: str) -> dict:
        return {PROGRESS_URL_FIELDS.ID : media_id}