import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent

CONTACTS_PER_PAGE = 10


def configure_argument_parser() -> argparse.ArgumentParser:
    """
    Конфигурирует аргументы командной строки.

    :return argparse.ArgumentParser: Объект ArgumentParser, настроенный
                                     с соответствующими аргументами.

    Аргументы командной строки:
    -c, --clear: Опция для очистки файла с данными.
                 При указании данной опции файл будет полностью очищен.
    -F, --fakedata N: Опция для заполнения базы данных указанным
                      количеством случайных записей. Аргумент N задает
                      количество случайных записей, которые нужно добавить
                      в базу данных.
    -f, --file: Опция для указания файла с данными.
                По умолчанию используется файл "contacts.txt".
    """
    parser = argparse.ArgumentParser(description="Телефонный справочник")
    parser.add_argument(
        "-c",
        "--clear",
        action="store_true",
        help="Очистить файл с данными"
    )
    parser.add_argument(
        "-F",
        "--fakedata",
        type=int,
        metavar="N",
        help="Заполнить базу данных N случайными записями",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="contacts.txt",
        help="Файл с данными"
    )
    return parser
