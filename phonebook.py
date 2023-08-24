import os
import re
from dataclasses import asdict, dataclass
from typing import List

from faker import Faker
from faker.providers import phone_number
from fuzzywuzzy import fuzz
from prettytable import PrettyTable

import constants
from configs import BASE_DIR

fake = Faker("ru_RU")
fake.add_provider(phone_number)


@dataclass
class Contact:
    last_name: str
    first_name: str
    middle_name: str
    organization: str
    work_phone: str
    personal_phone: str

    def __iter__(self):
        return iter(asdict(self).values())

    def __str__(self):
        return constants.CONTACT_OUTPUT_FORMAT.format(**asdict(self))


class PhoneBook:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.contacts = []

    def clear_file(self) -> None:
        with open(self.file_path, "w") as file:
            file.write("")

    def load_data(self) -> None:
        if not os.path.exists(self.file_path):
            (BASE_DIR / self.file_path).touch(exist_ok=True)

        with open(self.file_path, "r") as file:
            contacts = file.readlines()

        for contact in contacts:
            match = re.match(constants.FILE_FORMAT, contact)
            if match:
                contact = Contact(*match.groups())
                self.contacts.append(contact)

    def save_data(self) -> None:
        with open(self.file_path, "w") as file:
            for contact in self.contacts:
                line = str(contact) + "\n"
                file.write(line)

    def add_contact(
        self,
        last_name: str,
        first_name: str,
        middle_name: str,
        organization: str,
        work_phone: str,
        personal_phone: str,
    ) -> None:
        contact = Contact(
            last_name,
            first_name,
            middle_name,
            organization,
            work_phone,
            personal_phone,
        )
        self.contacts.append(contact)
        self.save_data()

    def edit_contact(
        self, contact: Contact, field_name: str, new_value: str
    ) -> bool:
        if field_name not in constants.CLASS_FIELDS:
            print("Недействительное поле для изменения")
            return False
        setattr(contact, field_name, new_value)
        phone_book.save_data()
        return True

    def search_contacts(self, search_query: str, field: str) -> List[Contact]:
        results = []
        for contact in self.contacts:
            value = getattr(contact, field)
            similarity = fuzz.ratio(
                search_query.lower().strip(), value.lower()
            )
            if similarity >= constants.SEARCH_THRESHOLD:
                results.append(contact)
        return results

    def print_contacts(self, page: int = 0, limit: int = 10) -> None:
        table = PrettyTable()
        table.field_names = ["№"] + constants.FIELDS
        output_contacts = self.contacts[page * limit: (page + 1) * limit]
        for index, contact in enumerate(output_contacts, start=1):
            table.add_row(
                [index + page * limit] + [value for value in contact]
            )
        print(table)

    def fill_database(self, num_records: int) -> None:
        for _ in range(num_records):
            last_name = fake.last_name()
            first_name = fake.first_name()
            middle_name = fake.first_name()
            organization = fake.company()
            work_phone = fake.phone_number()
            personal_phone = fake.phone_number()
            self.add_contact(
                last_name,
                first_name,
                middle_name,
                organization,
                work_phone,
                personal_phone,
            )
            self.save_data()

    def __len__(self) -> int:
        return len(self.contacts)
