import logging
import os
from logging.handlers import RotatingFileHandler

# create logs folder if not exists
LOG_DIR = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logger(name="AgentEngine"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # capture everything in development

    # prevent duplicate handlers
    if not logger.handlers:
        # 1. Console Handler (for printing in the terminal)
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        console_handler.setFormatter(console_format)
        
        # 2. File Handler (for saving in a file)
        file_handler = RotatingFileHandler(
            os.path.join(LOG_DIR, 'engine.log'), maxBytes=5000000, backupCount=3
        )
        file_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(file_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# global object that can be used anywhere
logger = setup_logger()
