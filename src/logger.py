# src/logger.py
import logging
import sys
from pathlib import Path

# (Optional) create logs directory
Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("tickethub")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler (optional, uncomment if you want to log to file as well)
# file_handler = logging.FileHandler("logs/app.log")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
