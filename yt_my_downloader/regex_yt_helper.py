import re

class RegexYtMatcher():
    # Latest: https://regex101.com/r/tJvDHf/1
    # Based on https://regex101.com/r/OY96XI/1 by mi-ca
    PATTERN = r"^(?:https?:)?(?:\/\/)?(?:(?:www\.|m\.)?youtube(?:-nocookie)?\.com\/(?:v\/|e\/|embed\/|w\/|(?:watch\?v=|(?:(?:\?|watch\?)(?:[\w]+=[\w]+&?)+)&v=)?|shorts\/)|youtu\.be\/(?:watch\?v=)?)([\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['\"][^<>]*>|<\/a>))[?=&+%\w.-]*$"
    result = None

    def __init__(self, input_str):
        self.result = re.search(string=input_str, pattern=self.PATTERN)

    def is_valid_yt_media_url(self) -> bool:
        return bool(self.result)
    
    def get_media_id(self):
        try:
            return self.result.group(1)
        except Exception() as e:
            return None
