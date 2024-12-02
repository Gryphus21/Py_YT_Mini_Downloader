REQUEST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.961.38 Safari/537.36 Edg/93.0.961.38', # Fake UA
    'Accept': 'application/json;charset=UTF-8', # Se implementato lato server evita imprecazioni
    'Accept-Encoding': 'identity', # Nessun metodo di compressione
    'Cache-Control': 'no-cache' # No Cache per il server
}

VIDEO_FILENAME = 'video.{}'.format('mp4')