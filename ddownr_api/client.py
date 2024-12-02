import urllib3
from urllib3 import ProxyManager
import os
import sys
from pprint import pprint

# For Exceptions
from urllib3.connectionpool import HTTPSConnectionPool
from urllib3.exceptions import NewConnectionError
import socket

import json
import time
import traceback

from colorama import Fore

import my_custom_print.my_custom_print as mcp

from ddownr_api.url import UrlMaker
from ddownr_api.video import VideoResolution
import ddownr_api.generic_downloader as gd
import ddownr_api.consts as consts
from ddownr_api.response_status import DownloadProgressResponse
from ddownr_api.response_status import RequestVideoDownloadResponse
from ddownr_api.response_status import DownloadStatus
from ddownr_api.request_handler import RequestHandler


PY_FILE_CURRENT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

class Client():
    """
        Classe che implementa un API che permette di sfruttare l'implementazione server di "https://ddownr.com" per scaricare video YouTube in locale.
    """

    pool = urllib3.PoolManager()
    use_https: bool = True

    def __init__(self, proxy: ProxyManager = None, use_https: bool = True):
        self.use_https = use_https
        if (proxy is not None):
            mcp.debug('Use proxy settings...')
            self.pool = proxy

    def _request_video_download_on_server(self, media_url: str, video_resolution: VideoResolution) -> RequestVideoDownloadResponse:
        xhr_download_url = UrlMaker.get_download_url(self.use_https)
        xhr_download_url_fields = UrlMaker.get_download_url_fields(media_url=media_url, video_resolution=video_resolution)
        #mcp.debug(xhr_download_url)
        #mcp.pprint(xhr_download_url_fields)
        #r = RequestHandler()

        try:
            response = self.pool.request(method='GET', headers=consts.REQUEST_HEADER, url=xhr_download_url, fields=xhr_download_url_fields)
            #mcp.debug(type(response.headers)) # urllib3._collections.HTTPHeaderDict
            #mcp.debug(type(response.connection)) # NoneType
            #mcp.debug(type(response.data)) # bytes
            
            #CAUT: Potrebbero scaturire eccezioni non gestite per possibili caratteri Unicode nella server response
            #TODO: Aggiungere un controllo nel caso il server inviasse dei caratteri Unicode
            #TODO: Verificare se il server restituisce HTML o nessun payload in base anche al HTTP STATUS CODE
        except socket.gaierror as e:
            mcp.print_red('Impossibibile connettersi al server (socket)\n')
            mcp.print_red(traceback.format_exc())
            exit()
        except urllib3.exceptions.NewConnectionError as e:
            mcp.print_red('Impossibibile connettersi al server (NewConnectionError)\n')
            mcp.print_red(traceback.format_exc())
            exit()
        except urllib3.exceptions.MaxRetryError as e: #TODO: Migliorare la gestione dell'eccezione Errorno 11001
            mcp.print_red('Impossibibile connettersi al server (MaxRetryError)\n')
            mcp.print_red(traceback.format_exc())

            reason: NewConnectionError = e.reason
            pool: HTTPSConnectionPool = e.pool
            mcp.debug(reason) # urllib3.exceptions.NewConnectionError
            mcp.debug(e.args) # tuple
            mcp.debug(pool) # urllib3.connectionpool.HTTPSConnectionPool
            mcp.debug(e.url) # str
            mcp.print_red(traceback.format_exc())
            exit()
        except Exception as e:
            mcp.print_red('Eccezione gestita ma non identificata\n')
            mcp.print_red(traceback.format_exc())
            exit()
        
        mcp.debug('_request_video_download_on_server():')
        mcp.debug(f'HTTP status: {response.status}')
        mcp.debug(f'payload: {response.data}')

        if (response.status == 200 and response.data is not None):
            try:
                json_obj = json.loads(response.data.decode('utf-8'))
                download_server_response_json_obj = RequestVideoDownloadResponse(_json_obj=json_obj, **json_obj)
            except json.decoder.JSONDecodeError as e:
                mcp.print_red('JSONDecodeError\n')
                mcp.print_red(traceback.format_exc())
                mcp.debug(f'Content decoded:\n{response.data.decode("utf-8")}')
                exit()
            except TypeError as e:
                mcp.print_red('TypeError\n')
                mcp.print_red(traceback.format_exc())
                mcp.debug(f"server response decoded: {response.data.decode('utf-8')}")
                exit()
            except Exception as e:
                mcp.print_red('Eccezione gestita ma non identificata\n')
                mcp.print_red(traceback.format_exc())
                exit()
        else:
            raise Exception('Problemi con la risposta del server in _request_video_download_on_server()')

        return download_server_response_json_obj
    
    def __get_download_progress(self, download_id: str) -> DownloadProgressResponse:
        #xhr_progress_url = UrlMaker.make_progress_url(download_id, self.use_https)
        xhr_progress_url = UrlMaker.get_progress_url(self.use_https)
        xhr_progress_url_fields = UrlMaker.get_progress_url_fields(download_id)
        #mcp.debug(download_id)
                                
        #WARN: Possibili eccezioni per:
        # urllib.error.URLError: <urlopen error [WinError 10065] Tentativo di operazione del socket verso un host non raggiungibile>
        # urllib.error.URLError: <urlopen error [Errno 11001] getaddrinfo failed>
        #CAUT: Possono esserci eventuali codici di stato HTTP di tipo 5XX, come 500 (Internal Server Error), 521 (No Reason Phrase), 502 (Bad Gateway); alcune di queste possono non avere il payload
        #TODO: Modificare prima la classe DownloadProgressResponse, aggiungere i codici di stato HTTP ed altre info di request()
        try:
            response = self.pool.request(method='GET', headers=consts.REQUEST_HEADER, url=xhr_progress_url, fields=xhr_progress_url_fields)
        except socket.gaierror as e:
            mcp.print_red('Impossibibile connettersi al server (socket)\n')
            mcp.print_red(traceback.format_exc())
            exit()
        except urllib3.exceptions.NewConnectionError as e:
            mcp.print_red('Impossibibile connettersi al server (NewConnectionError)\n')
            mcp.print_red(traceback.format_exc())
            exit()
        except urllib3.exceptions.MaxRetryError as e:#TODO: Migliorare la gestione dell'eccezione Errorno 11001
            mcp.print_red('Impossibibile connettersi al server (MaxRetryError)\n')
            mcp.print_red(traceback.format_exc())

            reason: NewConnectionError = e.reason
            pool: HTTPSConnectionPool = e.pool
            mcp.debug(reason) # urllib3.exceptions.NewConnectionError
            mcp.debug(e.args) # tuple
            mcp.debug(pool) # urllib3.connectionpool.HTTPSConnectionPool
            mcp.debug(e.url) # str
            mcp.print_red(traceback.format_exc())
            exit()
        except Exception as e:
            mcp.print_red('Eccezione gestita ma non identificata\n')
            mcp.print_red(traceback.format_exc())
            exit()

        try:
            json_obj = json.loads(response.data.decode('utf-8'))
            download_progress_response = DownloadProgressResponse(_json_obj=json_obj, **json_obj)
        except json.decoder.JSONDecodeError as e:
            mcp.print_red('JSONDecodeError\n')
            mcp.print_red(f'response.data: {response.data}\n\n')
            mcp.print_red(f"response.data.decode: {response.data.decode('utf-8')}\n")
            mcp.print_red(traceback.format_exc())
            exit()
        except TypeError as e:
            mcp.print_red('TypeError\n')
            mcp.print_red(traceback.format_exc())
            mcp.debug(f"server response decoded: {response.data.decode('utf-8')}")
            exit()
        except Exception as e:
            mcp.print_red('Eccezione gestita ma non identificata\n')
            mcp.print_red(f'response.data: {response.data}\n\n')
            mcp.print_red(f"response.data.decode: {response.data.decode('utf-8')}\n")
            mcp.print_red(traceback.format_exc())
            exit()
        return download_progress_response
    
    def _get_download_progress(self, download_id: str) -> DownloadProgressResponse:
        return self.__get_download_progress(download_id)

    def _get_download_progress(self, response: RequestVideoDownloadResponse) -> DownloadProgressResponse:
        return self.__get_download_progress(response.id)
        
    
    def _download_video_when_ready(self, response: RequestVideoDownloadResponse, downloading_path: str) -> bool:
        try: 
            #TODO: Questi valori devono già essere verificati
            success: int = int(response.success) # Tipicamente intero (0, 1) [Potrebbe essere anche 'false' nel caso si inviasse una richiesta senza parametro ?id=]
            progress_text: str = response.text # Tipicamente stringa o null
            #progress_percent: int = int(response.progress)/10 # Tipicamente intero (da 0 a 1000)
            download_url: str = response.download_url # Tipicamente stringa o null
        except ValueError as e:
            mcp.print_red('Eccezione gestita come ValueError')
            mcp.print_red(traceback.format_exc())
        except Exception as e:
            mcp.print_red('Eccezione gestita ma non identificata')
            mcp.print_red(traceback.format_exc())
            
        if (bool(success) and progress_text == 'Finished'):
            mcp.print_cyan('Il video sta per essere scaricato in locale...')
            mcp.debug(f'[_download_video_when_ready()] download url: {download_url}')
            
            dest_path = downloading_path + '\\' + consts.VIDEO_FILENAME
            process_status = gd.downloader(download_url, dest_path)

            #TODO: Mantenere il CompletedProcess all'interno di generic_downloader.py
            if process_status.returncode == 0:
                mcp.print_green(f'Il video è stato scaricato correttamente in locale in: {dest_path}\n')
            else:
                mcp.print_red(f'Problemi durante lo scaricamento del video, EXT: {process_status.returncode}\n')

            #TODO: Questa roba qui non mi piace, trovare un'altra soluzione
            return process_status.returncode
        else:
            return False
        

    def _show_download_status(self, progress_response: DownloadProgressResponse):
        try: 
            #TODO: Questi valori devono già essere verificati
            success: int = int(progress_response.success) # Tipicamente intero (0, 1) [Potrebbe essere anche 'false' nel caso si inviasse una richiesta senza parametro ?id=]
            progress_text: str = progress_response.text # Tipicamente stringa o null
            progress_percent: int = int(progress_response.progress)/10 # Tipicamente intero (da 0 a 1000)
            download_url: str = progress_response.download_url # Tipicamente stringa o null
        except ValueError as e:
            mcp.print_red('Eccezione gestita come ValueError')
            mcp.print_red(traceback.format_exc())
        except Exception as e:
            mcp.print_red('Eccezione gestitama non identificata')
            mcp.print_red(traceback.format_exc())
        
        if (progress_text is None): # 'null'
            mcp.print_cyan('Pre-Initialising (null)')
        elif (progress_text == 'error'):
            mcp.print_red('Errore imprevisto sul server')
            mcp.debug(f'progress_text: {progress_text}')
        elif (progress_text == 'Initialising'):
            mcp.print_cyan('Il video sta per essere scaricato sul server di terzi (Initialising)')
            mcp.print_cyan(f'Progress: {progress_percent}%')
        elif (progress_text == 'Downloading'):
            mcp.print_cyan('Il video è in scaricamento sul server di terzi (Downloading)')
            mcp.print_cyan(f'Progress: {progress_percent}%')
        elif (progress_text == 'Converting'):
            mcp.print_cyan('Il video è stato scaricato sul server di terzi e sta per essere convertito (Converting)')
            mcp.print_cyan(f'Progress: {progress_percent}%')
        elif (bool(success) and download_url is None):
            mcp.print_red('Il download è terminato ma non vi è nessun URL da cui scaricare il contenuto')
            mcp.debug(f'success: {success}')
            mcp.debug(f'download_url: {download_url}')
        elif (bool(success) and progress_text == 'Finished'):
            mcp.print_cyan('Video scaricato sul server di terzi (Finished)')
        else:
            mcp.print_red('Caso limite in _show_download_status()')
            mcp.debug(f'success: {success}')
            mcp.debug(f'download_url: {download_url}')
            mcp.debug(f'Response decoded:\n{progress_response}\n')
        print('\n')

    """
        Permette di scaricare il Video YT attraverso un URL valido per YT.

        Parameters:
        -----------
    """
    #TODO: Aggiungere tutti i controlli sui parametri
    #CAUT: Possibili eccezioni in caso di parametri errati
    def download_video_sync(self, media_url: str, downloading_path: str = PY_FILE_CURRENT_DIR, video_resolution: VideoResolution = VideoResolution.MP4_720P) -> DownloadStatus:
        req_video_download_resp = self._request_video_download_on_server(media_url, video_resolution)
        while True:
            download_progress_response = self._get_download_progress(req_video_download_resp)
            self._show_download_status(download_progress_response)
            local_download_result = self._download_video_when_ready(download_progress_response, downloading_path)
            if (local_download_result is not False):
                return True
            time.sleep(1)