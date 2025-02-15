from typing import Union

#TODO: Aggiungere un controllo sul tipo restituito dal server nel JSON.
#WARN: Nel caso il server restituisse qualcos'altro, la classe non sarà in grado funzionare correttamente.

class Undefined():
    def __str__(self):
        return 'Undefined'
    

class BasicMembers():
    pass


class ResponseCommonMembers(BasicMembers):
    _json_obj = None

    success: Union[int, bool] = int() # Generalmete int ma pùo essere anche bool

    def __init__(self, 
                 _json_obj = None,
                 success = Undefined()):

        self._json_obj = _json_obj
        self.success = success
        

class RequestVideoDownloadResponse(ResponseCommonMembers):
    id: str = str()
    title: str = str()
    #----------
    image: str = str()
    title: str = str()
    info: list = [image, title]
    #----------
    content: str = str()
    cachehash: str = str()
    repeat_download: bool = bool()
    message: str = str()
    #----------
    errors: dict = {} # "string": ["string"]
    additional_info: str = str() # default: null
    # ---------

    def __init__(self, 
                 _json_obj = None, 

                 success = Undefined(), 
                 id = Undefined(), 
                 content = Undefined(), 
                 title = Undefined(), 
                 info = Undefined(),
                 cachehash = Undefined(),
                 repeat_download = Undefined(), #NOTE: "false" in caso di YT url errato oppure durante il primo scaricamento, generalmente non definito nel JSON
                 message = Undefined(),
                 errors = Undefined(),
                 additional_info = Undefined()
                 ):
        
        super().__init__(_json_obj=_json_obj, success=success)

        self.id = id
        self.title = title
        self.info = info
        self.content = content
        self.cachehash = cachehash
        self.repeat_download = repeat_download
        self.message = message
        self.errors = errors
        self.additional_info = additional_info

# Richiesta corretta (già scaricato): success:1, progress:1000, download_url:"https://...", text:"Finished", message:"If you want..."
# Richiesta con id errato: success:0, progress:0, download_url:null, text:null, message:"If you want..."
# Richiesta priva di valore di chiave "id=": success:false, message:"Download id not found" #NOTE: Perchè scrive l'errore nel message ?
# Richiesta priva di query: success:false, message:"Id not found" #NOTE: Perchè scrive l'errore nel message ?
# Richiesta con "id=" di un download di video non esistente: success:1, progress:1000, download_url:null, text:"Video Unavailable", message:"If you want..." #NOTE: Perchè nel text ????!!!!

class DownloadProgressResponse(ResponseCommonMembers):
    progress: int = int()
    message: str = str()
    download_url:str = str()
    text: str = str()

    def __init__(self, 
                 _json_obj = None,

                 success = Undefined(), 
                 progress = Undefined(), 
                 download_url = Undefined(),
                 text = Undefined(),
                 message = Undefined()):
        
        super().__init__(_json_obj=_json_obj, success=success)

        self.progress = progress
        self.message = message
        self.download_url = download_url
        self.text = text


class DownloadProgress():
    PRE_INIT = None
    ERROR = 'error'
    INITIALISING = 'Initialising'
    DOWNLOADING = 'Downloading'
    CONVERTING = 'Converting'
    FINISHED = 'Finished'

class DownloadStatus():
    _response: RequestVideoDownloadResponse = None
    status: bool = False
    info: str = str()
    exception_title: str = None
    exception_traceback: str = None
    exception_infos: str = None

    def __init__(self, status: bool, info: str, response: RequestVideoDownloadResponse, exception_title: str = 'Eccezione gestita ma non identificata', exception_traceback: str = None, exception_infos: str = None):
        self.status = status
        self.info = info

        self.exception_title = exception_title
        self.exception_traceback = exception_traceback
        self.exception_infos = exception_infos
        