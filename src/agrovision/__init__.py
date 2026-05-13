import sys

from loguru import logger

logger.remove()  # remove default stderr sink
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss} | {level:<8} | {name} | {message}")
