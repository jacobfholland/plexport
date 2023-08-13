import coloredlogs
import logging
import os


class AutoFlushStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


def setup_logging():
    coloredlogs.install()
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    if LOG_DIR == "logs":
        logging.warning(
            "No custom LOG_DIR set. Defaulting to logs directory.")
    LOG_LEVEL = os.getenv("LOG_LEVEL").lower()
    log_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "critical": logging.CRITICAL,
        "error": logging.ERROR
    }
    LOG_LEVEL = log_levels.get(LOG_LEVEL)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_filename = os.path.join(LOG_DIR, 'plexport.log')
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, mode='w'),
            AutoFlushStreamHandler()
        ]
    )
