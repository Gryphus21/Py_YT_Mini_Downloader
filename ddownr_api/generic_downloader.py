import urllib

import subprocess
from subprocess import CompletedProcess
import os

import my_custom_print.my_custom_print as mcp



def _curl_process(url: str, destination_path: str) -> CompletedProcess:   
    return subprocess.run(['curl', '-o', destination_path.encode('utf-8'), url])

def _show_exit_status(process: CompletedProcess, destination_path: str):
    if (process.returncode == 18):
        mcp.debug(f'Il file "{destination_path}" non è stato scaricato completamente')
        if (os.path.isfile(destination_path)):
            os.remove(destination_path)
            mcp.debug(f'Il file {destination_path} è stato rimosso')
        else:
            mcp.debug(f'Nessun file "{destination_path}" rimosso perchè inesistente')
    elif (process.returncode == 23): #NOTE: Error Code: Failure writing output to destination
        mcp.debug(f'Problemi con il percorso di destinazione')

def _curl_downloader_implementation(url: str, destination_path: str) -> CompletedProcess:
    process = _curl_process(url, destination_path)
    _show_exit_status(process, destination_path)
    return process

def downloader(url: str, destination_path: str) -> CompletedProcess:
    #TODO: Sistemare l'esecuzione di CURL come comando esterno.
    #TODO: CURL non accetta caratteri UniCode nel percorso del file di destinazione, sistemare questo problema.
    #CAUT: Problema di caratteri UniCode nel percorso di destinazione, questo genera codici di uscita 23.
    #CAUT: Nel caso curl non riuscisse a terminare correttamente lo scaricamento, il file incompleto rimarrà ugualmente salvato, come se nulla fosse (Code 18).
    
    #mcp.debug(f'[_curl_downloader()] destination_path: {destination_path}')
    return _curl_downloader_implementation(url, destination_path)