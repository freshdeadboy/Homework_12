import pickle
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass    

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Invalid phone number format")
        self._value = new_value

class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format (use YYYY-MM-DD)")        
        self._value = new_value

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
        else:
            raise ValueError(f"Phone {old_phone} not found in the record")

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            return (next_birthday - today).days
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.value if self.birthday else 'N/A'}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, batch_size=5):
        records = list(self.data.values())
        for i in range(0, len(records), batch_size):
            yield records[i:i + batch_size]

    def save_to_file(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found. Creating a new address book.")
            self.data = {}

    def search(self, query):
        query = query.lower()
        matching_records = [record for record in self.data.values() if query in record.name.value.lower()]
        return matching_records