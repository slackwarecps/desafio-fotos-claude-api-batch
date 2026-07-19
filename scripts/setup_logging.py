"""
Setup de logging para os scripts do projeto
"""

import os
import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name, log_file=None):
    """Configura logger com arquivo + console"""
    
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = LOG_DIR / f"{name}_{timestamp}.log"
    else:
        log_file = LOG_DIR / log_file
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger, log_file

