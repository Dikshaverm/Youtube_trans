import yt_dlp
from datetime import datetime
import os
import youtube_dl
import sys
from youtube_translator.exception import YoutubeException
from youtube_translator.logger import logging


# Define download options
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"


os.makedirs(os.path.join(os.getcwd(), 'audio'), exist_ok=True)

filename = os.path.join(os.getcwd(), 'audio', filename)



ydl_opts2 = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(title)s.%(ext)s',
}


def download_audio1(youtube_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True  # Download only the single video
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename


if __name__ == '__main__':
        download_audio1('https://youtu.be/KcTal2LF-C8?si=un7aBj1GsI-Fxo1J' ,'C:\Project_min')