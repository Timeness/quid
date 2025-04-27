import os
from yt_dlp import YoutubeDL

async def download_audio(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_path = ydl.prepare_filename(info['entries'][0])
        title = info['entries'][0]['title']
        return file_path, title
