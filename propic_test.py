import json
import os
import traceback
from urllib.parse import urlparse, parse_qs
from typing import Union
import logging, requests, timeit

import yt_dlp as youtube_dl
from colorama import init as colorama_init
from colorama import Fore, Style

import ddownr_api
from ddownr_api import VideoResolution

import my_custom_print.my_custom_print as mcp

import yt_my_downloader as ytd
from yt_my_downloader.regex_yt_helper import RegexYtMatcher

import time

colorama_init()





def check_folder_exist_and_make(folder_path: str):
    """
        Verifica se la cartella esiste, se non esiste la crea.

        Parameters:
        -----------
            folder_path (str): Il percorso da controllare.
    """
    try:
        if (not os.path.isdir(folder_path)):
            os.mkdir(folder_path)
    except OSError as e:
        mcp.print_red('Eccezione OSError con Win error: ' + str(e.winerror))
        mcp.print_red(f'folder_path: {folder_path}')

        if (e.winerror == 123):
            print('Sintassi del nome della cartella presenta caratteri non validi')

        mcp.print_red(traceback.format_exc())
        exit()
    except Exception as e:
        mcp.print_red(traceback.format_exc())
        exit()

def file_exist(file_path: str) -> bool:
    return os.path.isfile(file_path)




