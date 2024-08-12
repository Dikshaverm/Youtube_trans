import yt_dlp
from datetime import datetime
import os
from pathlib import Path


# Define download options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


main_file_path = Path(os.path.abspath(os.path.join(os.getcwd(), '../../')))
print(f"Main file path : {main_file_path}")

audio_file_path = main_file_path / 'audio'
audio_file_path.mkdir(parents=True, exist_ok=True)
print(f"Audio file path : {audio_file_path}")

filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
output_path = audio_file_path / filename
print('filename: ', output_path)

ydl_opts2 = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': str(output_path),  # Ensure output path is a string
    'noplaylist': True  # Download only the single video
}

new = str('%(title)s.%(ext)s')

ydl_opts3 = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': new,  # Ensure output path is a string
    'noplaylist': True  # Download only the single video
}


def download_audio1(youtube_url):
    with yt_dlp.YoutubeDL(ydl_opts3) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        return ydl.prepare_filename(info_dict)


if __name__ == '__main__':
    download_audio1(youtube_url='https://youtu.be/KcTal2LF-C8?si=un7aBj1GsI-Fxo1J')
