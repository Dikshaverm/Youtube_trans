from flask import Flask, request, render_template
import torch
import whisper

from googletrans import Translator
import urllib.request
import os
from pydub import AudioSegment

app = Flask(__name__)

# Load the large Whisper model
model = whisper.load_model("large")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe(url=None, ):
    url = request.form[url]
    language = request.form['language']
    
    # Download the MP3 file
    mp3_file = "file.mp3"
    wav_file = "file.wav"
    urllib.request.urlretrieve(url, mp3_file)

    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format='wav')

    # Transcribe the audio file
    result = model.transcribe(wav_file)
    transcription = result["text"]

    # Translate the transcription
    translator = Translator()
    translation = translator.translate(transcription, dest=language).text

    # Remove the downloaded and converted audio files
    os.remove(mp3_file)
    os.remove(wav_file)

    return render_template('index.html', transcription=transcription, translation=translation)

if __name__ == '__main__':
    app.run(debug=True)