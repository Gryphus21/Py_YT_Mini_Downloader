from enum import Enum

from colorama import Fore

import yt_my_downloader.http_utils as httputils
import my_custom_print.my_custom_print as mcp



THUMBNAILS_BASE_URLS = [
    'https://{}.ytimg.com/vi/{}/sddefault.jpg',
    'https://{}.ytimg.com/vi/{}/hqdefault.jpg',
    'https://{}.ytimg.com/vi/{}/maxresdefault.jpg'
]

class THUMBNAIL_RESOLUTION(Enum):
    SD=0,
    HD=1,
    MAX=2

def get_subdomain_name(n: int) -> str:
    return 'i' if n==0 else str('i'+n)

#TODO: Sistemare in caso di errore di sito offline iX
def download_video_thumbnails(video_id: str, destination_path: str, video_thumbnail_resolution: THUMBNAIL_RESOLUTION = None):
    if (video_thumbnail_resolution is None):
        for thumb_base_url in THUMBNAILS_BASE_URLS:
            subdomain_counter = 0
            if (subdomain_counter <= 4):
                subdomain = get_subdomain_name(subdomain_counter)
                url = thumb_base_url.format(subdomain, video_id)
                mcp.debug(f'url formatted:{url}')
                if (not httputils.download_from_url(url, destination_path)):
                    mcp.print_red(f'\nScaricamento di "{url}" fallito')
                    subdomain_counter+=1
            else:
                raise Exception(f'{Fore.RED}Il thumbnail richiesto non è stato scaricato da nessuno degli indirizzi, possibili cause: nessuna connessione, nessun indirizzo raggiungibile (impossibile)')
    else:
        raise Exception(f'{Fore.RED}Non è stata specificata nessuna risoluzione di Thumbnails')