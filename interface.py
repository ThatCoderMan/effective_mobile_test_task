import argparse
import logging
import os
import re
from prettytable import PrettyTable
from configs import BASE_DIR, CONTACTS_PER_PAGE
from faker import Faker
from faker.providers import phone_number
from dataclasses import dataclass, asdict
import constants
from phonebook import PhoneBook


def print_menu():
    print("Меню:")
    for option, description in constants.MENU_OPTIONS.items():
        print(f"{option}. {description}")


def input_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Пожалуйста, введите целое число.")


def input_field(field_name):
    while True:
        value = input(f"{field_name}: ")
        if re.match(r'^[\w\s-]+$', value):
            return value
        else:
            print("Пожалуйста, введите корректное значение.")


def input_phone(field_name):
    while True:
        value = input(f"{field_name}: ")
        if re.match(
                r'^(\+7|8)?(\s|\()?(\d{3})(\s|\))?(\d{3})(\s|\-|\))?(\d{2})(\s|\-)?(\d{2})$',
                value):
            return value
        else:
            print("Пожалуйста, введите корректное значение.")


def add_new_contact(phone_book):
    print("Добавление новой записи в справочник:")
    last_name = input_field("Фамилия")
    first_name = input_field("Имя")
    middle_name = input_field("Отчество")
    organization = input("Название организации: ")
    work_phone = input_phone("Телефон рабочий")
    personal_phone = input_phone("Телефон личный")
    phone_book.add_contact(
        last_name,
        first_name,
        middle_name,
        organization,
        work_phone,
        personal_phone
    )
    print("Запись успешно добавлена.")


def edit_contact(phone_book):
    index = input_integer("Введите номер записи: ") - 1
    if 0 <= index < len(phone_book):
        contact = phone_book.contacts[index]
        for index, field in enumerate(constants.CLASS_FIELDS, start=1):
            value = getattr(contact, field)
            print(f"{index}. {field}: {value}")
        field_index = input_integer(
            "Введите индекс поля, которое хотите отредактировать:") - 1
        if field_index in [0, 1, 2]:
            new_value = input_field("Введите новое значение поля")
        elif field_index == 3:
            new_value = input("Введите новое значение поля: ")
        elif field_index in [4, 5]:
            new_value = input_phone("Введите новое значение поля")
        else:
            print("Некорректный индекс поля.")
            return
        field_name = constants.CLASS_FIELDS[field_index]
        if phone_book.edit_contact(contact, field_name, new_value):
            print("Значение поля успешно отредактировано.")
    else:
        print("Номер записи некорректный.")


def delete_contact(phone_book):
    print("Удаление записи из справочника:")
    index = input_integer("Введите номер записи: ") - 1
    if 0 <= index < len(phone_book.contacts):
        contact = phone_book.contacts.pop(index)
        print(f"Запись {str(contact).strip()} успешно удалена.")
    else:
        print("Номер записи некорректный.")
    phone_book.save_data()


def search_contacts(phone_book):
    for index, field in enumerate(constants.FIELDS, start=1):
        print(f"{index}. {field}")
    field_index = input_integer(
        "Введите индекс поля, по которому хотите произвести поиск:"
    ) - 1
    try:
        field = constants.CLASS_FIELDS[field_index]
    except IndexError:
        print('Некорректный индекс поля.')
        return
    search_query = input("Введите поисковой запрос: ")
    print(search_query, field)
    results = phone_book.search_contacts(search_query, field)
    if results:
        print("Результаты:")
        for index, contact in enumerate(results, start=1):
            print(f"{index}. {str(contact).strip()}")
    else:
        print("Записей не найдено.")


def menu(phone_book: PhoneBook):
    while True:
        print_menu()
        match input_integer("Выберите пункт меню: "):
            case 1:
                page = 1
                last_page = (len(phone_book)-1) // CONTACTS_PER_PAGE + 1
                while True:
                    phone_book.print_contacts(
                        page - 1,
                        limit=CONTACTS_PER_PAGE
                    )
                    print("Страница:", page)
                    if page != 1:
                        print("1. Назад")
                    if page != last_page:
                        print("2. Вперед")
                    print("3. Выход")
                    match input_integer("Выберите действие: "):
                        case 1:
                            if page > 1:
                                page -= 1
                            else:
                                print("Вы находитесь на первой странице.")
                        case 2:
                            if page < last_page:
                                page += 1
                            else:
                                print("Вы находитесь на последней странице.")
                        case 3:
                            break
                        case _:
                            print("Некорректный выбор.")
            case 2:
                add_new_contact(phone_book)
            case 3:
                edit_contact(phone_book)
            case 4:
                delete_contact(phone_book)
            case 5:
                search_contacts(phone_book)
            case 6:
                return
            case _:
                print("Некорректный выбор.")
