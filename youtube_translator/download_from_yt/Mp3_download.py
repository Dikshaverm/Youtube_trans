import yt_dlp
from datetime import datetime
from pathlib import Path
import pygame
from youtube_translator.logger import logging
from pydub import AudioSegment
from youtube_translator.exception import YoutubeException
from youtube_translator import constants
import sys


"""# Define download options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}"""


# main_file_path = Path(r"C:\Users\savit\PycharmProjects\Youtube_translator")

print(f"Main file path : {constants.MAIN_FILE_PATH}")

# audio_file_path = main_file_path / 'audio'

constants.AUDIO_FILE_PATH.mkdir(parents=True, exist_ok=True)
print(f"Audio file path : {constants.AUDIO_FILE_PATH}")


filename = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
AUDIO_OUTPUT_PATH = constants.AUDIO_FILE_PATH / filename

print('filename: ', AUDIO_OUTPUT_PATH)

ydl_opts2 = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': str(AUDIO_OUTPUT_PATH),  # Ensure output path is a string
    'noplaylist': True,  # Download only the single video
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
}


class AudioDownloader:
    def __init__(self, url):
        try:
            self.url = url
            self.output_path = AUDIO_OUTPUT_PATH
            logging.info(f"Storing the audio file in location : {self.output_path}\n")
            self.ydl_opts2 = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': str(self.output_path),  # Ensure output path is a string
                'noplaylist': True,  # Download only the single video
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            self.wav_file_path = str(self.output_path)+'.wav'
            print(f"Audio file wav path : {self.wav_file_path}")

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

    def download_audio(self):
        try:
            with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
                info_dict = ydl.extract_info(self.url, download=True)
                return ydl.prepare_filename(info_dict)

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

    def convert_audio(self):
        try:
            audio = AudioSegment.from_mp3(Path(self.audio_path()))
            audio.export(self.get_wav_path(), format="wav")
            logging.info(f"Converted audio file {self.output_path}")
            print(f"Converted audio file {self.get_wav_path()}")
            return audio

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

    def audio_path(self):
        try:
            actual_path = str(self.output_path) + '.mp3'
            print(f"Actual audio file path in mp3: {actual_path}")
            return actual_path

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)

    def get_wav_path(self):
        try:
            actual_path = self.wav_file_path
            print(f"Converted audio file wav path {actual_path}")
            return actual_path

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys)


#def download_audio(youtube_url):
 #   with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
   #     info_dict = ydl.extract_info(youtube_url, download=True)
  #      return ydl.prepare_filename(info_dict)


"""def audio_path():
    actual_path = str(AUDIO_OUTPUT_PATH)+'.mp3'
    return actual_path


if __name__ == '__main__':
    download_audio(youtube_url='https://youtu.be/KcTal2LF-C8?si=un7aBj1GsI-Fxo1J')
    pygame.mixer.init()
    pygame.mixer.music.load(Path(audio_path()))
    # pygame.mixer.music.load(r"C:\savit\PycharmProjects\Youtube_translator\audio\Exercise 1 Chapter 1 ： Python tutorial 10.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass
"""
