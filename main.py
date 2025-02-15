import json
import os
import traceback
#from urllib.parse import urlparse, parse_qs
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

#DONE: Aggiungere lo scaricamento delle Thumbnails
#TODO: Aggiungere lo scaricamento della Gif
#DONE: Aggiungere lo scaricamento della ProPic
#TODO: Convertire gli indirizzi dei percorsi per renderli compatibili con unix

#TODO: Aggiungere un sistema asincrono per eventuali liste di media
#TODO: Unificare tutte le stringhe contenenti URL in oggetti URL [MAI]
#TODO: Translate all comments in english


logging.basicConfig(level=logging.DEBUG, format="%(message)s")
os.chdir(os.path.dirname(os.path.abspath(__file__)))


MAIN_PATH_LOCATION = 'E:' if os.path.isdir('E:') else os.getcwd()
DOWNLOAD_FOLDER_NAME = 'YT_Downloaded'
VIDEO_FOLDER_NAME = 'Videos'
THUMBNAILS_FOLDER_NAME = 'Thumbnails'
DOWNLOAD_FOLDER_PATH = MAIN_PATH_LOCATION + '\\' + DOWNLOAD_FOLDER_NAME

VIDEO_YT_URL_MASK = 'https://www.youtube.com/watch?v={}'

JSON_FILENAME = 'media_infos.json'
URL_LIST_FILENAME = 'urls.txt'
URL_LIST_FILE_PATH = MAIN_PATH_LOCATION + '\\' + DOWNLOAD_FOLDER_NAME + '\\' + URL_LIST_FILENAME


SHORTCUT_BROWSER_FILENAME = 'Video Link'
SHORTCUT_BROWSER_FILE_EXT = '.url'


def replace_win_banned_char_for_path(text: str) -> str:
    """
        Sostituisce i caratteri bannati da Windows Explorer \ / : * ? " < > | per i nomi delle cartelle o files con [X].

        Parameters:
        -----------
            text (str): Il nome della cartella o file da controllare.
        
        Return:
        -------
            str: Il nome con l'eventuale sostituzione dei caratteri mostrati prima.
        
    """
    BANNED_CHAR_LIST = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    REPLACE_CHAR = '[X]'

    for banned_char in BANNED_CHAR_LIST:
        if banned_char in text:
            text = text.replace(banned_char, REPLACE_CHAR)
    return text

def if_too_long_for_path(text: str, media_id: str) -> str:
    """
        Sostituisce il nome del media con il media_id se è più lungo di 40 caratteri; per evitare problemi col filesystem di Windows per nomi o path troppo lunghi.

        Parameters:
        -----------
            text (str): Il nome del media.
            media_id (str): Il suo ID.

        Return:
        -------
            str: Restituisce un testo personalizzato che indica il numero di caratteri del nome del media, con il suo media_id per poter identificare il media.
    """
    return f'NAME TOO LONG [{len(text)}] - {media_id}' if len(text) > 40 else text

def uni_replacer(input_str: str) -> str:
    output_str = str()
    for c in input_str:
        if (len(c.encode('utf-8')) > 1):
            output_str += '[U]'
        else:
            output_str += c
    return output_str

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

def get_media_metadata_youtubedl(media_url: str) -> str:
    """
        Ottiene i metadati di un YouTube Video da "https://youtube.com" mediante il modulo "youtube_dl".

        Parameters:
        -----------
            media_url (str): Il URL del media.

        Return:
        -------
            str: JSON string con i metadati del media.
    """
    ydl = youtube_dl.YoutubeDL()
    return ydl.extract_info(media_url, download=False)

def save_to_json_file(json_file_path: str, json_obj: object): #JSON
    """
        Salva l'oggetto JSON su una posizione locale.

        Parameters:
        -----------
            json_file_path (str): Il percorso locale in cui si desidera salvare il file JSON.
            json_obj (object): Il JSON Object che si desidera salvare in locale.

    """
    try:
        with open(json_file_path, 'w') as f:
            json.dump(json_obj, f, indent=4)
    except Exception as e:
        mcp.print_red('Eccezione gestita sconosciuta')
        mcp.print_red(traceback.format_exc())
        exit()


class MediaDescriptor():
    """
        Raccolta di infomazioni per descrivere il media mediante URL e ID.

        Constants:
        ---------
            media_id (str): Conserva il ID del media (XXXXXXXXXXX).
            media_url (str): Conserva il URL del media compreso di ID nella url-query (https://www.youtube.com/watch?v=XXXXXXXXXXX).
    """
    media_id = str()
    media_url = str()
    
    def __init__(self, media_id: str, media_url: str) -> None:
        self.media_id = media_id
        self.media_url = media_url

def check_if_yt_id(input_str: str) -> bool:
    return (input_str.isascii() and len(input_str) == 11)

def get_mdl_from_user_input() -> Union[list[MediaDescriptor], list]: # media descriptor list
    """
        Permette l'acquisizione dei URL dei media dall'utente, che si desiderano scaricare.

        Return:
        -------
            list(MediaDescriptor) | list: Restituisce una lista di MediaDescriptor nel caso fossero stati acquisiti dal'utente, altimenti una lista vuota.
    """
    print(f"{Fore.CYAN}Inserisci gli {Fore.BLUE}URL{Fore.CYAN} o gli {Fore.BLUE}ID{Fore.CYAN} dei media{Fore.RESET}, {Fore.CYAN}quando hai finito 'Enter' (blank) per continuare{Fore.RESET}")
    
    media_descriptor_list = list()
    media_id = str()
    while True:
        mcp.print_white('\nDigita ID o URL, Enter per uscire:')
        input_str = input()
        if (input_str == ''):
            if media_descriptor_list:
                mcp.print_green("Ok procedo...\n")
            else:
                mcp.print_red("Nessun elemento inserito\n")

            return media_descriptor_list
        else:
            reg_helper = RegexYtMatcher(input_str)
            if reg_helper.is_valid_yt_media_url():
                media_id = reg_helper.get_media_id()
                media_url = input_str
            elif (check_if_yt_id(input_str)):
                media_id = input_str
                media_url = VIDEO_YT_URL_MASK.format(input_str)
            else:
                mcp.print_red("L'elemento inserito non è un URL, ne un ID di YouTube valido\n")
                continue
            del reg_helper

            media_descriptor_list.append(MediaDescriptor(media_id, media_url))

def get_lines_from_file(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines

def get_mdl_from_urls_file() -> Union[list[MediaDescriptor], list]:
    media_descriptor_list = list()
    lines_checking = list()

    lines = get_lines_from_file(URL_LIST_FILE_PATH)
    for pos, line in enumerate(lines):
        line_re = RegexYtMatcher(line)
        valid_line = line_re.is_valid_yt_media_url()
        lines_checking.append({'regular':valid_line, 'pos':pos+1, 'line':line})
        if (valid_line):
            media_id = line_re.get_media_id()
            media_url = line
            media_descriptor_list.append(MediaDescriptor(media_id, media_url))
    
    mcp.print_cyan(f'Report:')
    for line in lines_checking:
        color = Fore.GREEN if line['regular'] else Fore.RED
        p_line = f'{Style.BRIGHT}[Linea vuota]' if len(line['line']) == 0 else line['line']
        print(f"   {Fore.BLUE}Riga: {line['pos']} - {color}{p_line}{Style.RESET_ALL}")


    return media_descriptor_list

def get_mdl() -> Union[list[MediaDescriptor], list]:
    """
        Serve per ottenere la lista di MediaDescriptor dall'utente o da un file locale.

        Parameters:
        -----------
            use_file (bool): Indica se si vuole utilizzare il file locale oppure no.

        Return:
        -------
            list[MediaDescriptor]: Lista di MediaDescriptor acquisiti dall'utente o dal file (se use_file = True).
    """
    use_file = False
    if file_exist(URL_LIST_FILE_PATH):
        mcp.print_white(f'Vuoi caricare da file "{URL_LIST_FILENAME}" in "{URL_LIST_FILE_PATH}" ? (y):')
        use_file = True if input().lower()=='y' else False
    
    if (use_file):
        #TODO: Aggiungere un file cache in caso di eccezioni, per non perdere gli URL inseriti.
        mcp.print_cyan(f'\nProcedo a caricare il file...')
        media_descriptor_list = get_mdl_from_urls_file()
    else:
        media_descriptor_list = get_mdl_from_user_input()

    return media_descriptor_list

def channel_name_to_path(channel_name: str) -> str:
    """
        Converte il nome di un canale in un nome accetatto da Windows File System
        Verifica se:
            Il nome non è NoneType ([UnnamedChannel])
            Il nome è più lungo di 20 caratteri ([TooLongChannelName])
            Vertifica se il nome inizia o termina con carattere Spazio, in quel caso ingloba il nome dentro parentesi quadre

        Parameters:
        -----------
            channel_name (str): Il nome del canale.

        Return:
        -------
            str: Il nome del canale modificato se necessario.
    """
    if (channel_name is None):
        return '[UnnamedChannel]'
    elif (len(channel_name) > 20):
        return '[TooLongChannelName]'
    else:
        return f'[{channel_name}]' if channel_name.startswith(' ') or channel_name.endswith(' ') else channel_name

def channel_name_to_url(channel_name: str) -> str:
    """
        Permette di usare il nome del canale con un indirizzo YT valido.

        Parameters:
        -----------
            channel_name (str): ID del canale.

        Return:
        -------
            str: URL con il nome del canale.
    """
    return f'https://www.youtube.com/{channel_name}'

def make_shortcut_link_file(media_url: str, shortcut_file_path: str):
        """
            Genera un file shortcut per il browser (in Windows) che permette di aprire direttamente il browser sul indirizzo Web specificato (il media YT in questo caso).

        Parameters:
        -----------
            media_url (str): Il URL del media.
            shortcut_file_path (str): Il percorso dove si desidera creare il file in locale.
        """

        FILE_CONTENT_TAMPLATE = '[InternetShortcut]\nURL={}\n'
        try:
            with open(shortcut_file_path, 'w') as f:
                f.write(FILE_CONTENT_TAMPLATE.format(media_url))
        except Exception as e:
            mcp.print_red('Eccezione gestita sconosciuta')
            mcp.print_red(traceback.format_exc())
            exit()


def download_channel_image(channel_url: str, destination_path: str):
    import filecmp
    import shutil

    TMP_PROPIC_FILENAME = 'tmp.jpg'
    tmp_propic_file_path = destination_path + '\\' + TMP_PROPIC_FILENAME

    PROPIC_FILENAME = 'propic.jpg'
    propic_file_path = destination_path + '\\' + PROPIC_FILENAME

    OLDPROPICS_FOLDER_NAME = 'Oldests'
    oldpropics_folder_path = destination_path + '\\' + OLDPROPICS_FOLDER_NAME

    def get_last(path) -> int:
        last = 0

        for element in os.listdir(path):
            elem_name: str = os.path.splitext(os.path.basename(element))[0]
            if os.path.isfile(path + '\\' + element) and elem_name.isdigit():
                #WARN: Se ci fossero altri files con nomi composti da lettere nella cartella sarebbero problemi grossi (Parzialmente risolto)
                #WARN: Se ci fosse un file di numero alto, il successivo file verrebbe rinominato con il numero successivo
                last = int(elem_name) # È un numero
        return last

    if file_exist(propic_file_path):
        first_download = False
        download_filename = TMP_PROPIC_FILENAME
    else:
        first_download = True
        download_filename = PROPIC_FILENAME

    if (ytd.download_channel_propic(channel_url, destination_path, download_filename)):
        if not first_download:
            if (not filecmp.cmp(tmp_propic_file_path, propic_file_path, shallow=False)):
                check_folder_exist_and_make(oldpropics_folder_path)
                old_file_path = destination_path + '\\' + str(get_last(oldpropics_folder_path)+1) + '.jpg'
                os.rename(propic_file_path, old_file_path) # Rinomina in 1,2,3... la propic già presente
                shutil.move(old_file_path, oldpropics_folder_path) # la sposta nella cartella Oldests
                os.rename(tmp_propic_file_path, propic_file_path) # Rinomina la tmp.jpg in propic.jpg
            else:
                os.remove(tmp_propic_file_path)
    else:
        raise Exception('Problemi durante lo scaricamento della propic')


#def get_query_value_from_url(url: str, query_key: str) -> str:
"""
        Ottiene il primo valore della chiave specificata, di una query in un URL.

        Parameters:
        -----------
            url (str): Url da analizzare.
            query_key (str): Il valore della chiave da cui si desidera prendere il valore.

        Return:
        -------
            str: Il valore della chiave specificata.
    """
#    parsed = urlparse(url)
#    return parse_qs(parsed.query)[query_key][0]

def file_exist(file_path: str) -> bool:
    return os.path.isfile(file_path)

def dir_exist(path: str) -> bool:
    return os.path.isdir(path)


#NOTE: Dovrebbe conservare solo i metadati scaricati dal modulo "youtube_dl".
class VideoMetadata():
    def __init__(self) -> None:
        pass

#NOTE: Dovrebbe conservare un insieme di oggetti per descrivere i metadati, lo stato del download ed altre informazioni.
class YouTubeMedia():
    def __init__(self) -> None:
        pass

class YouTubeVideo(YouTubeMedia):
    def __init__(self) -> None:
        pass

class YouTubeShorts(YouTubeMedia):
    def __init__(self) -> None:
        pass


def main():
    colorama_init()
    
    media_descriptor_list = get_mdl()
    if not media_descriptor_list:
        mcp.print_red('\nNessun dato è stato caricato, chiusura del programma.')
        exit()
    else:
        mcp.print_cyan('\nQuesti sono gli URL caricati:')
        for i, single in enumerate(media_descriptor_list):
            mcp.print_cyan(f'{i+1} - {single.media_url}')

    ddownr_client = ddownr_api.Client()

    #mcp.print_white('\nVuoi richiedere lo scaricamento di tutti i media (massivo), oppure scaricare tutto singolarmente (più lento) ? (y):')
    #input().lower() == 'y'
    if (False): #TODO: Adding timer for auto chose
        id_list = list()
        mcp.print_cyan('Scaricamento massivo...')
        #REFACT: Rifattorizzare qui
        for single_media in media_descriptor_list:
            #WARN: Se ci fossero problemi lato server o con le richieste ?
            id = ddownr_client._request_video_download_on_server(single_media.media_url, VideoResolution.MAX_RES_TEST_ONLY)
            mcp.debug(f'ID: {id}')
            id_list.append(id)
        if (len(id_list) != len(media_descriptor_list)):
            raise Exception('La quantità degli ID in "id_list" non corrispondono con quelli dei media richiesti da scaricare ("media_descriptor_list"), forse ci sarà qualche problema con le richieste HTTP o col server')
        
        mcp.print_green('Tutte le richieste di scaricamento sono state inviate')

        for single_id in id_list:
            mcp.print_green(f'id: {single_id}')
            ddownr_client._show_download_status(ddownr_client._get_download_progress(single_id))
    else:
        mcp.print_cyan('Scaricamento singolo...')
        for single_media in media_descriptor_list:
            mcp.print_cyan(f'\nInizio scaricamento per il media {single_media.media_url}...')
            mcp.print_cyan('Scaricamento dei Metadati...')
            result = get_media_metadata_youtubedl(single_media.media_url)
            mcp.print_green('Metadati scaricati\n')

            if 'entries' in result: # Nel caso fosse una Playlist
                media_json_str = result['entries'][0]
            else: # Altrimenti un media singolo
                media_json_str = result

            media_infos_json_obj = json.loads(json.dumps(media_json_str))

            check_folder_exist_and_make(DOWNLOAD_FOLDER_PATH)

            # Risoluzione del nome della cartella del canale e creazione
            #TODO: Unificare tutti i dati del media su un Oggetto
            #WARN: Possibile problemi con il nome del canale, se fosse troppo lungo o avesse caratteri strani
            #WARN: I nomi dei media possono iniziare con un carattere 'Spazio' ?
            #CAUT: Il nome del canale può essere 'zero width space'
            #CAUT: Possono esistere nomi molto lunghi +400 caratteri
            channel_name = media_infos_json_obj['channel']
            channel_name_path_abj = replace_win_banned_char_for_path(channel_name_to_path(channel_name))
            mcp.debug(f'channel_name:{channel_name}')
            mcp.debug(type(channel_name))
            channel_folder_path = DOWNLOAD_FOLDER_PATH + '\\' + channel_name_path_abj # Evita 'spazi' prima e dopo il nome canale per evitare problemi con Windows e soprattutto evita il NoneType
            check_folder_exist_and_make(channel_folder_path)

            # Risoluzione del nome della cartella del media e creazione
            #DONE: Aggiungere una verifica del nome Video se potrebbe creare problemi se usato come nome per una cartella
            #NOTE: Non rimuovere 'media_title_for_path'
            media_title_for_path = uni_replacer(replace_win_banned_char_for_path(media_infos_json_obj['title'])) #NOTE: Replace some unicode characters for avoid problems with CURL downloader
            media_folder_path = channel_folder_path + '\\' + media_title_for_path
            check_folder_exist_and_make(media_folder_path)
            
            # Cartella Videos
            media_subfolder_path = media_folder_path + '\\' + VIDEO_FOLDER_NAME
            check_folder_exist_and_make(media_subfolder_path)
            
            # Cartella Thumbnails
            media_thumbnail_folder = media_folder_path + '\\' + THUMBNAILS_FOLDER_NAME
            check_folder_exist_and_make(media_thumbnail_folder)

            # Salvataggio del JSON obj
            json_file_path = media_folder_path + '\\' + JSON_FILENAME
            mcp.print_cyan('Salvo i metadati in un file JSON...')
            save_to_json_file(json_file_path, media_infos_json_obj)
            mcp.print_green('File salvato\n')

            # Creazione di un file shortcut per il browser
            mcp.print_cyan('\nCreazione dello shortcut al media per il browser...')
            make_shortcut_link_file(single_media.media_url, media_folder_path+'\\'+SHORTCUT_BROWSER_FILENAME+SHORTCUT_BROWSER_FILE_EXT)
            mcp.print_green('Shortcut file creato\n')

            # Scaricamento delle Thumbnails
            mcp.print_cyan('Scaricamento delle Thumbnails del media...')
            mcp.debug(f'single_media.media_id: {single_media.media_id}')
            ytd.download_video_thumbnails(single_media.media_id, media_thumbnail_folder)
            mcp.print_green('Thumbnails del media scaricate\n')

            # Scaricamento della ProPic del Canale
            #TODO: Aggiungere un controllo nel caso si sovrascrivessere ProPic vecchie, già scaricate, con altre nuove
            #CAUT: Questo sovrascriverebbe le vecchie immagini di profilo scaricate in precedenza
            mcp.print_cyan('Scaricamento della ProPic...')
            mcp.debug(f'channel_folder_path: {channel_folder_path}')
            mcp.debug(f"channel url:{media_infos_json_obj['channel_url']}")
            download_channel_image(media_infos_json_obj['channel_url'], channel_folder_path)
            #ytd.download_channel_propic(media_infos_json_obj['channel_url'], channel_folder_path, 'propic.jpg')
            mcp.print_green('ProPic scaricata (forse)\n')


            mcp.print_cyan('Scaricamento del media...')
            #TODO: Problemi con caratteri UniCode nel percorso di destinazione, questo genererà un Exit Code 23 di CURL
            #CAUT: Possibile Exit Code 23 per CURL nel caso ci fosse un media o un canale con un carattere UniCode nel nome 
            #TODO: Aggiungere un controllo della risoluzione massima del media, per salvare il file con l'estensione corretta
            #CAUT: Se se sceglie una risoluzione che non è possibile scaricare, tipo un media che non ha il 144p; il server risponderà con un content vuoto, privo di JSON
            ddownr_client.download_video_sync(single_media.media_url, media_subfolder_path, VideoResolution.MP4_1440P)

            #del result
            #del media_json_str
            #del media_infos_json_obj

            mcp.print_green(f'Fine scaricamento per il media "{single_media.media_url}"')

if (__name__ == '__main__'):
    main()
else:
    raise Exception(f'{Fore.RED}Not main')