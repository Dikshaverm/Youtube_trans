from youtube_translator.logger import logging
from youtube_translator.download_from_yt.Mp3_download import AudioDownloader
from youtube_translator.db_storage import Mp3FileStorage
import streamlit as st
from youtube_translator.constants import lang_dict2
from youtube_translator.model.whisper_model import Transcribe
import uuid

if st.session_state is None:
    st.session_state.url = ''


with st.form(key='my-form'):
    url = st.text_input('Enter the URL')
    st.session_state.url = url

    language = st.radio('Select Language', lang_dict2.keys())
    st.session_state.language = language

    final_language = lang_dict2[language]
    st.session_state.final_language = final_language

    st.info("Selected Language: {}".format(final_language))
    submit = st.form_submit_button(label='Submit')


if submit:
    session_id = int(uuid.uuid4())

    audio_downloader = AudioDownloader(url)
    audio_downloader.download_audio()

    audio_file_path = audio_downloader.audio_path()
    audio_downloader.convert_audio()

    wav_file_path = audio_downloader.get_wav_path()

    file_name = str(uuid.uuid4())

    file_storage = Mp3FileStorage()
    file_storage.insert_mp3_file(session_id=session_id,
                                 file_path=audio_file_path,
                                 file_name=file_name
                                 )
    logging.info(f"File Inserted in database successfully {file_name}")

    file_storage.delete_mp3_file_from_os(file_path=audio_file_path)
    logging.info(f"File deleted from OS successfully {file_name}")

    audio_data = file_storage.get_mp3_file(session_id=session_id, file_name=file_name)

    file_storage.delete_mp3_file_from_os(file_path=wav_file_path)

    # Model
    trans = Transcribe()
    st.session_state.transcript = trans.voice_to_text(audio_data)
    logging.info(f"Transcribe successfully {file_name}")

    file_storage.delete_wav_file_from_os(file_path=wav_file_path)
    logging.info("Deleting the wav file from storage")

    st.markdown("## TEXT TRANSCRIPT")
    st.write(st.session_state.transcript)

    st.session_state.final_text = trans.translate_text(text=st.session_state.transcript, language_code=final_language)
    st.markdown("### Translated Text")
    st.write(st.session_state.final_text)





