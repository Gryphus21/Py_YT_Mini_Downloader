# Py YT Mini Downloader
Python program that will allow you to download videos from YouTube using external services.

## Using
It will allow you to download videos in various resolutions (if allowed), such as 360p, 480p, 720p, 1080p, 1440p and 4K.
The downloaded files will be sorted into folders in the directory where the program is located.
You can enter the ID or URL of the YouTube video.

## Folders structure
YT_Downloaded
├── urls.txt (List of URL to download, created by user, one URL or Video ID per line)
└── *YouTube Channel Name*
    ├── propic.jpg (YouTube channel profile picture)
    ├── Oldests (Not always present)
    │   └── [number]*.jpg (Previously downloaded old profile pictures)
    └── *YouTube Video Title*
        ├── Thumbnails
        │   ├── hqdefault.jpg (If exists)
        │   ├── maxresdefault.jpg (If exists)
        │   └── sddefault.jpg (If exists)
        ├── Videos
        │   └── video.mp4
        ├── media_infos.json (Media infos in JSON format)
        └── Video Link.url (Link to the YT Video)

## Notice:
The external services used are:
- [ddownr.com](https://ddownr.com) for downloading videos
- [ytimg.com](https://ytimg.com) for downloading video thumbnail
- [contentforest.com](https://contentforest.com) for downloading channel profile picture