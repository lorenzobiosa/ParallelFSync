import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE

def setup_logger():
    logger = logging.getLogger("ParallelFSync")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=100_000_000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
