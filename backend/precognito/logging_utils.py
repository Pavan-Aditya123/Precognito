import logging
import sys
from pythonjsonlogger import json

def setup_logging():
    """Sets up structured JSON logging for the application.

    Configures the root logger with a StreamHandler that outputs JSON-formatted
    logs to stdout. Also silences overly verbose third-party loggers.
    """
    handler = logging.StreamHandler(sys.stdout)
    formatter = json.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    # Silence overly verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
