from pathlib import Path


lang_dict = {'bn': 'bengali' ,
             'en': 'english' ,
             'gu': 'gujarati',
             'hi': 'hindi',
             'kn': 'kannada',
             'ml': 'malayalam',
             'mr': 'marathi',
             'ne': 'nepali',
             'pa': 'punjabi',
             'ta': 'tamil',
             'te': 'telugu',
             'fr': 'french'}

lang_dict.keys()
lang_dict.values()

lang_dict2 = {}
for key, value in lang_dict.items():
    if key in lang_dict2:
        lang_dict2[value] = key
    else:
        lang_dict2[value] = key


MAIN_FILE_PATH = Path(r"C:\Users\savit\PycharmProjects\Youtube_translator")
AUDIO_FILE_PATH = Path(__file__).parent.with_name('audio')