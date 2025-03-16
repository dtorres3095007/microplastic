import logging
from datetime import date
import os


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    today = date.today()
    log_date = today.strftime("%Y-%m")
    logging.basicConfig(
        filename=f"logs/app_{log_date}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    return logging.getLogger(__name__)
