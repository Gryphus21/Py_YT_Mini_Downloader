class VideoSpecs():
    file_extension = None
    url_format = None

    def __init__(self, resolution: str, file_extension: str, url_format: str) -> None:
        self.resolution = resolution
        self.file_extension = file_extension
        self.url_format = url_format

class VideoResolution():
    MP4_360P = VideoSpecs('360', 'mp4', '360')
    MP4_480P = VideoSpecs('480', 'mp4', '480')
    MP4_720P = VideoSpecs('720', 'mp4', '720')
    MP4_1080P = VideoSpecs('1080', 'mp4', '1080')
    MP4_1440P = VideoSpecs('1440', 'mp4', '1440')
    WEBM_4K = VideoSpecs('3840', 'webm', '4k')
    
    # HIGHER = ''
    MAX_RES_TEST_ONLY = VideoSpecs('3840', 'mp4', '4k')