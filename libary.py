import csv
from datetime import datetime
from unidecode import unidecode
import re


class SanityCheck:
    def __init__(self):
        self.check_files("books.csv", "readers.csv", "history.csv")

    def check_files(self, *args):
        try:
            with open("books.csv", "r") as books_file:
                pass
        except FileNotFoundError:
            with open("books.csv", "w", newline="") as books_file:
                books_writer = csv.writer(books_file, delimiter=",")
                books_writer.writerow(["id", "title", "author", "year", "status"])

        try:
            with open("readers.csv", "r") as readers_file:
                pass
        except FileNotFoundError:
            with open("readers.csv", "w", newline="") as readers_file:
                readers_writer = csv.writer(readers_file, delimiter=",")
                readers_writer.writerow(["id", "name", "surname", "books_count"])

        try:
            with open("history.csv", "r") as history_file:
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
            print(f" Ksiazka juz istnieje.")
            return
        book_id = len(self.__books) + 1
        title = unidecode(title)  # Usuń polskie znaki
        author = unidecode(author)  # Usuń polskie znaki
        if not re.match(r'^[a-zA-Z\s]+$', author):
            print(f" Autor moze zawierać tylko litery i spacje.")
            return
        if not re.match(r'^\d+$', str(year)):
            print(f" Rok musi być liczba.")
            return
        new_book = Book(book_id, title, author, year, "W bibliotece")
        self.__books.append(new_book)
        self.__save_books_to_file()
        print(f"Ksiazka dodana do biblioteki.")

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
                if len(reader.get_borrowed_books()) >= 5 :
                    print(f" Czytelnik wypozyczyl juz maksymalna ilość ksiazek.")
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
            self.add_reader(reader_id, name, surname)  # Utwórz nowego czytelnika, jeśli nie zostal znaleziony

        book_found = False
        for book in self.__books:
            if book.get_title() == title:
                if book.get_status() == "Wypozyczona":
                    print(f" Ksiazka jest juz wypozyczona.")
                    return
                book_found = True
                book.set_status("Wypozyczona")
                book.add_to_borrow_history(reader_id, date)
                break

        if not book_found:
            print(f" Ksiazka nie istnieje.")
            return

        for reader in self.__readers:
            if reader.get_id() == reader_id:
                reader.add_borrowed_book(title)
                reader.increase_books_count()
                break

        self.__save_books_to_file()
        self.__save_readers_to_file()
        self.__save_history_to_file()
        print(f" Ksiazka wypozyczona.")


    def return_book(self, title, reader_id, date):
        if reader_id is None or title is None:
            print(f" Wszystkie dane (numer, tytul) musza być podane.")
            return
        if not re.match(r'^\d+$', str(reader_id)):
            print(f" ID musi być liczba.")
            return
        reader_id = int(reader_id)

        for reader in self.__readers:
            if reader.get_id() == reader_id:
                if title in reader.get_borrowed_books():
                    reader.remove_borrowed_book(title)
                    reader.decrease_books_count()
                else:
                    print(f" Czytelnik nie ma wypozyczonej ksiazki o tytule {title}.")
                    return

        for book in self.__books:
            if book.get_title() == title and book.get_status() == "Wypozyczona":
                if datetime.strptime(book.get_borrow_history()[-1][1], "%Y-%m-%d %H:%M:%S") > datetime.strptime(date, "%Y-%m-%d %H:%M:%S"):
                    print(f" Data oddania nie moze być wcześniejsza niz data wypozyczenia.")
                    return
                book.set_status("W bibliotece")
                book.get_borrow_history()[-1] = book.get_borrow_history()[-1] + (date,)
                self.__save_readers_to_file()
                self.__save_books_to_file()
                self.__save_history_to_file()
                print(f" Ksiazka oddana.")
                return

        print(f" Nie ma takiej ksiazki w bibliotece.")

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
        with open('history.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID ksiazki", "Numer czytacza", "Data wypozyczenia", "Data oddania"])
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
                    print(f"Historia wypozyczeń ksiazki {title}:")
                    for history in book.get_borrow_history():
                        print(f"Czytacz ID: {history[0]}, Data wypozyczenia: {history[1]}, Data zwrócenia: {history[2] if len(history) > 2 else 'Nie zwrócono jeszcze'}")
                else:
                    print(f"Ksiazka {title} nie byla jeszcze wypozyczona.")
                self.__save_history_to_file()  # add this line to save the history to file
                return
        print(f" Nie ma ksiazki o tytule {title}.")


    def __load_books_from_file(self):
        try:
            with open('books.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy naglówek
                for row in reader:
                    book_id, title, author, year, status = row
                    self.__books.append(Book(int(book_id), title, author, int(year), status))
        except FileNotFoundError:
            print(f" Brak pliku books.csv. Utworzono nowa listę ksiazek.")


    def __load_history_from_file(self):
        try:
            with open('history.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy naglówek
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
                        print(f" W historii znaleziono nieprawidlowe ID czytelnika: {reader_id}")
        except FileNotFoundError:
            print(f" Brak pliku history.csv. Utworzono nowa listę historii wypozyczeń.")

    def __load_readers_from_file(self):
        try:
            with open('readers.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy naglówek
                for row in reader:
                    reader_id, name, surname, books_count = row
                    self.__readers.append(Reader(int(reader_id), name, surname, int(books_count)))
        except FileNotFoundError:
            print(f" Brak pliku readers.csv. Utworzono nowa listę czytelników.")


def menu():
    library = Library()

    while True:
        print(f"MENU")
        print("1. Dodaj ksiazkę")
        print("2. Wypozycz ksiazkę")
        print("3. Zwróć ksiazkę")
        print("4. Historia ksiazki")
        print("5. Wyjdź")

        option = input("Wybierz opcję: ")

        if option == "1":
            title = input("Podaj tytul ksiazki: ")
            author = input("Podaj autora ksiazki: ")
            try:
                year = int(input("Podaj rok wydania ksiazki: "))
                if year > datetime.now().year or not str(year).isdigit():
                    print(f" Rok wydania nie moze być większy niz {datetime.now().year}.")
                    continue
            except:
                print(f" Rok wydania musi być liczba.")
                continue
            library.add_book(title, author, year)
        elif option == "2":
            title = input("Podaj tytul ksiazki do wypozyczenia: ")
            reader_id = input("Wprowadź numer ID czytelnika: ")
            if not reader_id.isdigit():
                print(f" ID musi być liczba.")
                continue
            reader_id = int(reader_id)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            library.lend_book(title, reader_id, date)
        elif option == "3":
            title = input("Podaj tytul ksiazki do zwrócenia: ")
            reader_id = input("Podaj numer czytelnika zwracajacego ksiazkę: ")
            if not reader_id.isdigit():
                print(f" ID musi być liczba.")
                continue
            reader_id = int(reader_id)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            library.return_book(title, reader_id, date)
        elif option == "4":
            title = input("Podaj tytul ksiazki, której historię chcesz sprawdzić: ")
            library.book_history(title)
        elif option == "5":
            break
        else:
            print(f" Nieprawidlowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    SanityCheck().check_files()
    menu()
