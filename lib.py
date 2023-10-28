from collections import UserDict
import re
import calendar
from collections import defaultdict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not re.match(r"\d{10}", value):
            raise ValueError

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
            raise ValueError

        birthday = value.split(".")

        super().__init__(
            date(int(birthday[2]), int(birthday[1]), int(birthday[0])))


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phone = None
        self.birthday = None

    def set_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def set_phone(self, phone: str):
        self.phone = Phone(phone)

    def __str__(self):
        return f"{self.name.value}: {self.phone.value}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data[name]

    def delete(self, name: str):
        self.data.pop(name)

    def get_birthdays(self):
        today = datetime.today().date()

        output_data = defaultdict(list)

        for name in self.data:
            if not self.data[name].birthday:
                continue

            birthday = self.data[name].birthday.value

            celebration_date = birthday.replace(year=today.year)

            if celebration_date < today:
                celebration_date = celebration_date.replace(
                    year=today.year + 1)

            delta_to_celebration = celebration_date - today

            if delta_to_celebration.days >= 7:
                continue

            if celebration_date.weekday() in [5, 6]:
                celebration_date = celebration_date + \
                    timedelta(days=7 - celebration_date.weekday())

            output_data[celebration_date.weekday()].append(name)
            sorted(output_data)

        output = []

        for weekday_index in output_data.keys():
            day_name = calendar.day_name[weekday_index]
            celebrator_names = ", ".join(output_data.get(weekday_index))

            output.append(f"{day_name}: {celebrator_names}")

        return output
