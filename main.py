import streamlit as st
from youtube_translator.constants import lang_dict2

import os
from youtube_translator.model import download_audio

"""if st.session_state is None:
    st.session_state.lang = 'en'
if st.session_state['download'] is None:
    st.session_state['download'] = ''"""

st.markdown('## VIDEO TRANSLATOR')
st.title('Video Translator')

with st.form(key='my-form'):

    url2 = st.text_input('Enter the URL')
    st.session_state.url = url2

    language = st.radio('Select Language', lang_dict2.keys())
    st.session_state.language = language

    final_language = lang_dict2[language]
    st.session_state.final_language = final_language

    submit = st.form_submit_button(label='Submit')


if submit:
    st.write(st.session_state.url)
    st.write(st.session_state.language)
    st.write(f"Language code : {st.session_state.final_language}")

    st.session_state.downloaded_audio = download_audio(st.session_state.url)
    st.info(f"Audio file downloaded")

    with open(st.session_state.downloaded_audio, 'w') as audio_file:
        audio_file.write(st.session_state.downloaded_audio)

    os.makedirs(os.path.join(os.getcwd(), 'audio_files'), exist_ok=True)

    # os.path.join(st.session_state.downloaded_audio,  ).

    path_name = os.path.join(os.getcwd(), 'wav_files.wav')




