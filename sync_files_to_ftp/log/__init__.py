from loguru import logger

logger.add("log/debug.log", format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}", level="DEBUG", rotation="100 MB", compression="zip")