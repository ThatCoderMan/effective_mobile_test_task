import argparse
import logging
import os
import re
from prettytable import PrettyTable
from configs import configure_logging, configure_argument_parser, BASE_DIR
from faker import Faker
from faker.providers import phone_number
from dataclasses import dataclass, asdict
import constants
from interface import menu
from phonebook import PhoneBook


if __name__ == "__main__":
    configure_logging()
    parser = configure_argument_parser()
    args = parser.parse_args()

    phone_book = PhoneBook(args.file)

    if args.clear:
        phone_book.clear_file()

    phone_book.load_data()

    if args.fakedata:
        phone_book.fill_database(args.fakedata)
        phone_book.save_data()

    menu(phone_book)
