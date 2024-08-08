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


# Download the audio
st.cache_resource()
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
