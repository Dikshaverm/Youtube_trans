import os

from googletrans import Translator

from pydub import AudioSegment
from urllib import request
import streamlit as st
import whisper

import yt_dlp


# Define download options
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

from datetime import datetime

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
        'noplaylist': True,  # Download only the single video
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

download_audio1('https://youtu.be/KcTal2LF-C8?si=un7aBj1GsI-Fxo1J', r"C:\Users\savit\PycharmProjects\Youtube_translator\audio")




@st.cache_resource
def download_audio(url):
    global ydl_opts
    with os.path.join(os.makedirs(os.getcwd(),'rw', exist_ok=True),
                      yt_dlp.YoutubeDL(ydl_opts)) as ydl:
        audio = ydl.download([url])

        print('new', os.path.basename(audio))

    os.makedirs(os.path.join(os.getcwd(), 'data'), exist_ok=True)

    os.system('ffmpeg -i ' + os.path.join(os.getcwd(), 'data', audio) + '.mp4')
    return audio







def transcribe(url: str, language: str):
    # Download the MP3 file
    download_audio_file = download_audio(url)

    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(download_audio_file)
    audio.export(wav_file, format='wav')

    # Load the large Whisper model
    model = whisper.load_model("large")

    # Transcribe the audio file
    result = model.transcribe(wav_file)
    transcription = result["text"]

    # Translate the transcription
    translator = Translator()
    translation = translator.translate(transcription, dest=language).text

    os.remove(mp3_file)
    os.remove(wav_file)

    return translation, transcription
