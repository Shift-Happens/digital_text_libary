import csv
from datetime import datetime
from unidecode import unidecode
import re


class SanityCheck:
    def __init__(self):
        self.check_files("books.csv", "readers.csv", "history.csv")

    def check_files(self, *args):
        try:
            with open("books.csv", "r", encoding='utf-8') as books_file:
                pass
        except FileNotFoundError:
            with open("books.csv", "w", newline="", encoding='utf-8') as books_file:
                books_writer = csv.writer(books_file, delimiter=",")
                books_writer.writerow(["id", "title", "author", "year", "status"])

        try:
            with open("readers.csv", "r", encoding='utf-8') as readers_file:
                pass
        except FileNotFoundError:
            with open("readers.csv", "w", newline="", encoding='utf-8') as readers_file:
                readers_writer = csv.writer(readers_file, delimiter=",")
                readers_writer.writerow(["id", "name", "surname", "books_count"])

        try:
            with open("history.csv", "r", encoding='utf-8') as history_file:
                pass
        except FileNotFoundError:
            with open("history.csv", "w", newline="") as history_file:
                history_writer = csv.writer(history_file, delimiter=",")
                history_writer.writerow(["date", "error"])


class Book:
    def __init__(self, book_id, title, author, year, status):
        self.__id = book_id
        self.__title = title
        self.__author = author
        self.__year = int(year)
        self.__status = status
        self.__borrow_history = []

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def add_to_borrow_history(self, reader_id, borrow_date, return_date=None):
        if return_date is None:
            self.__borrow_history.append((reader_id, borrow_date))
        else:
            self.__borrow_history.append((reader_id, borrow_date, return_date))

    def get_borrow_history(self):
        return self.__borrow_history


class Reader:
    def __init__(self, reader_id, name, surname, books_count):
        self.__id = reader_id
        self.__name = name
        self.__surname = surname
        self.__books_count = int(books_count)
        self.__borrowed_books = []

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_books_count(self):
        return self.__books_count

    def get_borrowed_books(self):
        return self.__borrowed_books

    def increase_books_count(self):
        self.__books_count += 1

    def decrease_books_count(self):
        self.__books_count -= 1

    def add_borrowed_book(self, title):
        self.__borrowed_books.append(title)

    def remove_borrowed_book(self, title):
        self.__borrowed_books.remove(title)


class Library:
    def __init__(self):
        self.__books = []
        self.__readers = []
        self.__load_books_from_file()
        self.__load_readers_from_file()
        self.__load_history_from_file()

    def __is_unique_reader(self, reader_id, name, surname):
        for reader in self.__readers:
            if reader.get_id() == reader_id or (reader.get_name() == name and reader.get_surname() == surname):
                return False
        return True

    def __is_unique_book(self, title, author):
        for book in self.__books:
            if book.get_title() == title and book.get_author() == author:
                return False
        return True

    def write_error_to_history(self, error):
        with open("history.csv", "a", newline="") as history_file:
            history_writer = csv.writer(history_file, delimiter=",")
            history_writer.writerow([datetime.now(), error])

    def add_book(self, title, author, year):
        if not self.__is_unique_book(title, author):
            print(f" Książka już istnieje.")
            return
        book_id = len(self.__books) + 1
        title = unidecode(title)  # Usuń polskie znaki
        author = unidecode(author)  # Usuń polskie znaki
        if not re.match(r'^[a-zA-Z\s]+$', author):
            print(f" Autor może zawierać tylko litery i spacje.")
            return
        if not re.match(r'^\d+$', str(year)):
            print(f" Rok musi być liczbą.")
            return
        new_book = Book(book_id, title, author, year, "W bibliotece")
        self.__books.append(new_book)
        self.__save_books_to_file()
        print(f"Książka dodana do biblioteki.")

    def lend_book(self, title, reader_id, date):
        reader_id = int(reader_id)
        try:
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(f" Data musi być w formacie YYYY-MM-DD HH:MM:SS.")
            return
        reader_found = False
        for reader in self.__readers:
            if reader.get_id() == reader_id:
                if len(reader.get_borrowed_books()) >= reader.get_books_count():
                    print(f" Czytelnik wypożyczył już maksymalną ilość książek.")
                    return
                reader_found = True
                break

        if not reader_found:
            name = None
            surname = None
            while not name:
                name = input("Podaj imię czytelnika: ")
            while not surname:
                surname = input("Podaj nazwisko czytelnika: ")
            self.add_reader(reader_id, name, surname)  # Utwórz nowego czytelnika, jeśli nie został znaleziony

        book_found = False
        for book in self.__books:
            if book.get_title() == title:
                if book.get_status() == "Wypożyczona":
                    print(f" Książka jest już wypożyczona.")
                    return
                book_found = True
                book.set_status("Wypożyczona")
                book.add_to_borrow_history(reader_id, date)
                break

        if not book_found:
            print(f" Książka nie istnieje.")
            return

        for reader in self.__readers:
            if reader.get_id() == reader_id:
                reader.add_borrowed_book(title)
                reader.decrease_books_count()
                break

        self.__save_books_to_file()
        self.__save_readers_to_file()
        self.__save_history_to_file()
        print(f" Książka wypożyczona.")


    def return_book(self, title, reader_id, date):
        if reader_id is None or title is None:
            print(f" Wszystkie dane (numer, tytuł) muszą być podane.")
            return
        if not re.match(r'^\d+$', str(reader_id)):
            print(f" ID musi być liczbą.")
            return
        reader_id = int(reader_id)

        for reader in self.__readers:
            if reader.get_id() == reader_id:
                if title in reader.get_borrowed_books():
                    reader.remove_borrowed_book(title)
                    reader.increase_books_count()
                else:
                    print(f" Czytelnik nie ma wypożyczonej książki o tytule {title}.")
                    return

        for book in self.__books:
            if book.get_title() == title and book.get_status() == "Wypożyczona":
                if datetime.strptime(book.get_borrow_history()[-1][1], "%Y-%m-%d %H:%M:%S") > datetime.strptime(date, "%Y-%m-%d %H:%M:%S"):
                    print(f" Data oddania nie może być wcześniejsza niż data wypożyczenia.")
                    return
                book.set_status("W bibliotece")
                book.get_borrow_history()[-1] = book.get_borrow_history()[-1] + (date,)
                self.__save_readers_to_file()
                self.__save_books_to_file()
                self.__save_history_to_file()
                print(f" Książka oddana.")
                return

        print(f" Nie ma takiej książki w bibliotece.")

    def add_reader(self, reader_id, name, surname):
        name = unidecode(name)  # Usuń polskie znaki
        surname = unidecode(surname)  # Usuń polskie znaki
        new_reader = Reader(reader_id, name, surname, 0)
        self.__readers.append(new_reader)
        self.__save_readers_to_file()

    def __save_books_to_file(self):
        with open('books.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Tytul", "Autor", "Rok", "Status"])
            for book in self.__books:
                writer.writerow([book.get_id(), book.get_title(), book.get_author(), book.get_year(), book.get_status()])

    def __save_history_to_file(self):
        with open('history.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID książki", "Numer czytacza", "Data wypożyczenia", "Data oddania"])
            for book in self.__books:
                for history in book.get_borrow_history():
                    writer.writerow([book.get_id(), history[0], history[1], history[2] if len(history) > 2 else "Nie zwrócono jeszcze"])

    def __save_readers_to_file(self):
        with open('readers.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Numer czytacza", "Imie", "Nazwisko", "Ilosc ksiazek"])
            for reader in self.__readers:
                writer.writerow([reader.get_id(), reader.get_name(), reader.get_surname(), reader.get_books_count()])

    def book_history(self, title):
        for book in self.__books:
            if book.get_title() == title:
                if book.get_borrow_history():
                    print(f"Historia wypożyczeń książki {title}:")
                    for history in book.get_borrow_history():
                        print(f"Czytacz ID: {history[0]}, Data wypożyczenia: {history[1]}, Data zwrócenia: {history[2] if len(history) > 2 else 'Nie zwrócono jeszcze'}")
                else:
                    print(f"Książka {title} nie była jeszcze wypożyczona.")
                self.__save_history_to_file()  # add this line to save the history to file
                return
        print(f" Nie ma książki o tytule {title}.")


    def __load_books_from_file(self):
        try:
            with open('books.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy nagłówek
                for row in reader:
                    book_id, title, author, year, status = row
                    self.__books.append(Book(int(book_id), title, author, int(year), status))
        except FileNotFoundError:
            print(f" Brak pliku books.csv. Utworzono nową listę książek.")


    def __load_history_from_file(self):
        try:
            with open('history.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy nagłówek
                for row in reader:
                    book_id, reader_id, borrow_date, return_date = row
                    try:
                        for book in self.__books:
                            if book.get_id() == int(book_id):
                                if return_date == "Nie zwrócono jeszcze":
                                    book.add_to_borrow_history(int(reader_id), borrow_date)
                                else:
                                    book.add_to_borrow_history(int(reader_id), borrow_date, return_date)
                                break
                    except ValueError:
                        print(f" W historii znaleziono nieprawidłowe ID czytelnika: {reader_id}")
        except FileNotFoundError:
            print(f" Brak pliku history.csv. Utworzono nową listę historii wypożyczeń.")

    def __load_readers_from_file(self):
        try:
            with open('readers.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy nagłówek
                for row in reader:
                    reader_id, name, surname, books_count = row
                    self.__readers.append(Reader(int(reader_id), name, surname, int(books_count)))
        except FileNotFoundError:
            print(f" Brak pliku readers.csv. Utworzono nową listę czytelników.")


def menu():
    library = Library()

    while True:
        print(f"MENU")
        print("1. Dodaj książkę")
        print("2. Wypożycz książkę")
        print("3. Zwróć książkę")
        print("4. Historia książki")
        print("5. Wyjdź")

        option = input("Wybierz opcję: ")

        if option == "1":
            title = input("Podaj tytuł książki: ")
            author = input("Podaj autora książki: ")
            try:
                year = int(input("Podaj rok wydania książki: "))
                if year > datetime.now().year or not str(year).isdigit():
                    print(f" Rok wydania nie może być większy niż {datetime.now().year}.")
                    continue
            except:
                print(f" Rok wydania musi być liczbą.")
                continue
            library.add_book(title, author, year)
        elif option == "2":
            title = input("Podaj tytuł książki do wypożyczenia: ")
            reader_id = input("Wprowadź numer ID czytelnika: ")
            if not reader_id.isdigit():
                print(f" ID musi być liczbą.")
                continue
            reader_id = int(reader_id)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            library.lend_book(title, reader_id, date)
        elif option == "3":
            title = input("Podaj tytuł książki do zwrócenia: ")
            reader_id = input("Podaj numer czytelnika zwracającego książkę: ")
            if not reader_id.isdigit():
                print(f" ID musi być liczbą.")
                continue
            reader_id = int(reader_id)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            library.return_book(title, reader_id, date)
        elif option == "4":
            title = input("Podaj tytuł książki, której historię chcesz sprawdzić: ")
            library.book_history(title)
        elif option == "5":
            break
        else:
            print(f" Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    SanityCheck().check_files()
    menu()
