from logging import Logger
import subprocess
from os import path
import logging
from logging import handlers
from datetime import datetime, timedelta

APP_NAME = 'pveutils'

logger = None


def init():
    global logger
    if logger is None:
        logger = logging.getLogger(APP_NAME)
        logger.setLevel(logging.INFO)
        rf_handler = handlers.TimedRotatingFileHandler(path.join('/root/pveutils/logs', f'{APP_NAME}.log'), when='D', interval=1, backupCount=7)
        rf_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
        rf_handler.level = logging.INFO
        rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(rf_handler)
        st_handler = logging.StreamHandler()
        st_handler.level = logging.DEBUG
        st_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(st_handler)


init()


def run(cmd, echo=False):
    try:
        if echo:
            print(cmd)
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = e.output       # Output generated before error
        #code      = e.returncode   # Return code
    return str(result, encoding = "utf-8", errors='ignore')


def date_str(days=0):
    _date = datetime.now() + timedelta(days=days)
    return _date.strftime("%Y%m%d")