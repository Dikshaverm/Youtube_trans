from googletrans import Translator
import whisper
import sys
from youtube_translator.logger import logging
from youtube_translator.exception import YoutubeException
import streamlit as st

with st.spinner(text='Please wait Loading Whisper Large model...'):
    model = whisper.load_model(name='large')
    logging.info("Model loaded successfully")

st.info("Model loaded successfully")


class Transcribe:
    def __init__(self):
        self.model = model
        self.translator = Translator()

    def voice_to_text(self, voice_file_path):
        try:
            result = model.transcribe(voice_file_path)
            text = result['text']
            return text
        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys) from e

    def translate_text(self, text: str, language_code: str):
        try:
            trans = self.translator.translate(text, dest=language_code)
            text = trans.text
            return text

        except Exception as e:
            logging.error(e)
            raise YoutubeException(e, sys) from e


"""if __name__ == "__main__":
    whisper = Transcribe()
    text = whisper.voice_to_text(r"C:\savit\PycharmProjects\Youtube_translator\data\5960619c-f4ac-4020-8279-efb3ff9b9442_from_db.wav")
    print(text)
    print()
    text = whisper.translate_text(text, "en")
    print(text)"""
