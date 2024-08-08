from setuptools import setup, find_packages

PACKAGE_NAME = 'Youtube_translator'
PACKAGE_VERSION = '1.0.0'
AUTHOR = 'Diksha Verma'
AUTHOR_EMAIL = 'dikshavermaa8800@gmail.com'
URL = 'https://github.com/Dikshaverm/Youtube_trans.git'
VERSION = PACKAGE_VERSION
DESCRIPTION = 'Translate YouTube videos.'
LONG_DESCRIPTION = 'Translate YouTube videos.'
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(),
    include_package_data=True,
)