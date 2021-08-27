from logging import Logger
import subprocess
from os import path
import logging, time
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
        rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)7s - %(message)s"))
        logger.addHandler(rf_handler)
        st_handler = logging.StreamHandler()
        st_handler.level = logging.DEBUG
        st_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)7s - %(message)s"))
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

def D(*args):
    '''色彩打印 DEBUG
    '''
    _print('DEBUG', *args)


def I(*args):
    '''色彩打印 INFO
    '''
    _print('INFO', *args)


def E(*args):
    '''色彩打印 ERROR
    '''
    _print('ERROR', *args)


def _print(level, *args):
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if level == 'DEBUG':
        header = '1;33;44'
        fg = 33
    elif level == 'INFO':
        header = '5;34;43'
        fg = 32
    elif level == 'ERROR':
        header = '1;33;41'
        fg = 31
    else:
        header = '5;30;46'
        fg = 34
    app_header = '5;34;47'
    message = f'{local_time} \x1b[{app_header}m]\x1b[0m - \x1b[{header}m{level:5}\x1b[0m - \x1b[{fg}m'
    print(message, *args, )
    print('\x1b[0m', flush=True)
    
    
def print_color_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30, 38):
            s1 = ''
            for bg in range(40, 48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
                usage = f'Format: effect;foreground;background (Ex. \\x1b[{format}m {format} \\x1b[0m)'
    
            print(s1)
        print(usage)
    print()

if __name__ == '__main__':
    print_color_table()