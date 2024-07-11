# logging_config.py
import logging
import logging.config
from pathlib import Path

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging_config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": str(log_dir / "app.log"),
                "formatter": "default",
            },
            "excel_file": {
                "class": "logging.FileHandler",
                "filename": str(log_dir / "excel_file.log"),
                "formatter": "default",
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "": {  # root logger
                "level": "INFO",
                "handlers": ["file", "console"],
            },
            "excel_file_logger": {
                "level": "INFO",
                "handlers": ["excel_file", "console"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up.")
