from lib import AddressBook, Record
import pickle


def parse_input(user_input):
    cmd, *args = user_input.split()

    cmd = cmd.strip().lower()

    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Incorrect data provided."
        except KeyError:
            return "Contact not found"
        except IndexError:
            return "Give me the name please."

    return inner


@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args

    record = Record(name)

    record.set_phone(phone)

    contacts.add_record(record)

    return "Contact added."


@input_error
def change_contact(args, contacts: AddressBook):
    name, phone = args

    contacts[name].set_phone(phone)

    return f"Contact {name} changed."


def show_all_contacts(contacts: AddressBook):
    return "\n".join([f"{contacts[name]}" for name in contacts.keys()])


@input_error
def show_contact(args, contacts: dict):
    name = args[0]

    return contacts[name]


@input_error
def add_birthday(args, contacts):
    name, birthday = args

    contacts[name].set_birthday(birthday)

    return f"Contact {name} changed."


def show_birthday(args, contacts: AddressBook):
    name = args[0]

    return contacts[name].birthday.value.strftime("%d.%m.%Y")


def show_birthdays(args, contacts: AddressBook):
    return "\n".join(contacts.get_birthdays())


def main():
    try:
        with open('address_book.bin', 'rb') as file:
            book = pickle.loads(file.read())
    except:
        book = AddressBook()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            with open('address_book.bin', 'wb') as file:
                file.write(pickle.dumps(book))

            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_contact(args, book))
        elif command == "all":
            print(show_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(show_birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
