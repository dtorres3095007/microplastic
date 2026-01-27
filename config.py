import logging
from datetime import date
import os


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    today = date.today()
    log_date = today.strftime("%Y-%m")
    log_file = os.path.abspath(f"logs/app_{log_date}.log")
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Check if file handler already exists for this file
    file_handler_exists = False
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            try:
                # Compare absolute paths
                handler_path = os.path.abspath(handler.baseFilename)
                if handler_path == log_file:
                    file_handler_exists = True
                    break
            except (AttributeError, OSError):
                pass
    
    # Only add file handler if it doesn't exist
    if not file_handler_exists:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Ensure basicConfig is called if root logger has no handlers at all
    if not root_logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    return logging.getLogger(__name__)
