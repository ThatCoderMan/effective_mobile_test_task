import argparse
import logging
from logging.handlers import RotatingFileHandler

from pathlib import Path

BASE_DIR = Path(__file__).parent

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

DT_FORMAT = '%d.%m.%Y %H:%M:%S'

CONTACTS_PER_PAGE = 10


def configure_argument_parser():
    parser = argparse.ArgumentParser(description='Телефонный справочник')
    parser.add_argument(
        '-c',
        '--clear',
        action='store_true',
        help='Очистить файл с данными'
    )
    parser.add_argument(
        '-F',
        '--fakedata',
        type=int,
        metavar='N',
        help='Заполнить базу данных N случайными записями'
    )
    parser.add_argument(
        '-f',
        '--file',
        default='contacts.txt',
        help='Файл с данными'
    )
    return parser


def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parser.log'
    BASE_DIR.touch()
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
