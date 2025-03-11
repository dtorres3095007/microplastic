import logging

def setup_logger():
    logging.basicConfig(
        filename="app_local.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    return logging.getLogger(__name__)
