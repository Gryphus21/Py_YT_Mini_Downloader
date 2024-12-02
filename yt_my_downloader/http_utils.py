import time
import urllib
from urllib.parse import urlparse
import http
import traceback
import os

import yt_my_downloader as http_utils
import my_custom_print.my_custom_print as mcp

#TODO: Far restituire un oggetto Struct per verificare lo stato del download
def download_from_url(url: str, destination_path: str, filename: str = None) -> bool:
    if filename is None:
        url_parsed = urlparse(url)
        filename = os.path.basename(url_parsed.path)
    mcp.debug(f'[download_from_url()] Scaricamento di "{filename}"...')

    MAX_TRIES = 5
    tries = 1
    success = False
    while (tries <= MAX_TRIES and not success):
        try:
            urllib.request.urlretrieve(url=url, filename=destination_path+'\\'+filename)
            success = True
        except urllib.error.HTTPError as http_err:
            if http_err.code == 404:
                mcp.print_red(f'Il file "{filename}" non esiste (HTTP404)')
                return success
        except http.client.RemoteDisconnected as e:
            mcp.print_red(f'Errore durante lo scaricamento di "{url}"')
            mcp.print_red('La connessione è stata inaspettatamente interrotta senza nessuna risposta')
            mcp.print_red(f'{traceback.format_exc()}')
        except Exception as e:
            mcp.print_red(f'Errore durante lo scaricamento di "{url}"')
            mcp.print_red(f'Tentativo {tries} di {MAX_TRIES}')
            mcp.print_red(f'{traceback.format_exc()}')
            tries+=1
            time.sleep(1)
    if success:
        mcp.print_green(f'"{url}" scaricato\n')
        #mcp.debug(f'"{url}" scaricato\n')
    return success