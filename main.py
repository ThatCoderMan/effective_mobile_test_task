from configs import configure_argument_parser
from interface import menu
from phonebook import PhoneBook

if __name__ == "__main__":
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
