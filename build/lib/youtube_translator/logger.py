import logging
import os
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"


LOG_FILE_PATH = os.path.join(os.getcwd(), 'logs')
