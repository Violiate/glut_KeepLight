import os,sys
from loguru import logger


def init(version):
    logger.remove(handler_id=0)
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if sys.argv[0].endswith(".py"):
        debug = True
        level = "DEBUG"
        format = "DEBUG MODE | <green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"
        environment = "development"
        print("WARNING: YOU ARE IN DEBUG MODE")
    else:
        debug = False
        level = "INFO"
        format = "<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"
        environment = "production"
    handler_id = logger.add(
        sys.stderr,
        format=format,
        level=level,
        backtrace=debug,
        diagnose=debug,
    )
    logger.add(
        "./logs/{time:YYYYMMDD-HHmmss}.log",
        format=format,
        level="DEBUG",
        backtrace=True,
        diagnose=True,
        colorize=False,
        encoding="utf-8",
    )