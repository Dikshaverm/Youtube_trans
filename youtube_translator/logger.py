import logging
import os
import sys
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# main_file_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
main_file_path = r"C:\Users\savit\PycharmProjects\Youtube_translator"
sys.path.insert(0, main_file_path)

LOG_FILE_PATH = os.path.join(main_file_path, 'Logs_data', LOG_FILE_NAME)

os.makedirs(LOG_FILE_PATH, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_FILE_PATH, LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO,
                    format='%(asctime)s %(filename)s %(lineno)d - %(levelname)s - %(message)s')


logging.info(f'Logging started at {LOG_FILE_PATH}')