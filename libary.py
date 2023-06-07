import csv
from datetime import datetime
from unidecode import unidecode
import re


class SanityCheck:
    def __init__(self):
        self.check_files("biblioteka.csv", "czytacze.csv", "historia.csv")

    @staticmethod
    def check_files(self, *args):
        try:
            with open("biblioteka.csv", "r") as books_file:
                pass
        except FileNotFoundError:
            with open("biblioteka.csv", "w", newline="") as books_file:
                books_writer = csv.writer(books_file, delimiter=",")
                books_writer.writerow(["ID", "Tytul", "autor", "Rok wydania", "Status"])

        try:
            with open("czytacze.csv", "r") as readers_file:
                pass
        except FileNotFoundError:
            with open("czytacze.csv", "w", newline="") as readers_file:
                readers_writer = csv.writer(readers_file, delimiter=",")
                readers_writer.writerow(["Numer czytacza", "Imie", "Nazwisko", "Ilosc ksiazek"])

        try:
            with open("historia.csv", "r") as history_file:
                pass
        except FileNotFoundError:
            with open("historia.csv", "w", newline="") as history_file:
                history_writer = csv.writer(history_file, delimiter=",")
                history_writer.writerow(["ID", "Numer czytacza", "Czy udana", "Data wypozyczenia", "Data oddania"])
            # trzeba zaimplementowac te parametry do funkcji lend_book i return_book, dodac je do funkcji
            # add_to_borrow_history w klasie Book, oraz dodac je do funkcji __load_history_from_file w klasie Library
            # wtedy bedzie mozna zapisywac historie wypozyczen i oddan do pliku
            # historia.csv i odczytywac z niego historie wypozyczen i oddan przy uruchomieniu programu


class Book:
    def __init__(self, id_ksiazki, tytul, autor, rok_wydania, status):
        self.__id = id_ksiazki
        self.__tytul = tytul
        self.__autor = autor
        self.__rok_wydania = int(rok_wydania)
        self.__status = status
        self.__borrow_history = []

    def get_id(self):
        return self.__id

    def get_tytul(self):
        return self.__tytul

    def get_autor(self):
        return self.__autor

    def get_rok_wydania(self):
        return self.__rok_wydania

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

    def add_borrowed_book(self, tytul):
        self.__borrowed_books.append(tytul)

    def remove_borrowed_book(self, tytul):
        self.__borrowed_books.remove(tytul)


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

    def __is_unique_book(self, tytul, autor):
        for book in self.__books:
            if book.get_tytul() == tytul and book.get_autor() == autor:
                return False
        return True

    def write_error_to_history(self, error):
        with open("historia.csv", "a", newline="") as history_file:
            history_writer = csv.writer(history_file, delimiter=",")
            history_writer.writerow([datetime.now(), error])

    def add_book(self, tytul, autor, rok_wydania):
        if not self.__is_unique_book(tytul, autor):
            print(f" Ksiazka juz istnieje.")
            return
        id_ksiazki = len(self.__books) + 1
        tytul = unidecode(tytul)  # Usuń polskie znaki
        autor = unidecode(autor)  # Usuń polskie znaki
        if not re.match(r'^[a-zA-Z\s]+$', autor):
            print(f" Autor moze zawierać tylko litery i spacje.")
            return
        if not re.match(r'^\d+$', str(rok_wydania)):
            print(f" Rok musi być liczba.")
            return
        new_book = Book(id_ksiazki, tytul, autor, rok_wydania, "W bibliotece")
        self.__books.append(new_book)
        self.__save_books_to_file()
        print(f"Ksiazka dodana do biblioteki.")

    def lend_book(self, tytul, reader_id, date):
        reader_id = int(reader_id)
        try:
            datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            print(f" Data musi być w formacie YYYY-MM-DD HH:MM:SS.")
            return
        reader_found = False
        for reader in self.__readers:
            if reader.get_id() == reader_id:
                if len(reader.get_borrowed_books()) >= reader.get_books_count():
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
            if book.get_tytul() == tytul:
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
                reader.add_borrowed_book(tytul)
                reader.decrease_books_count()
                break

        self.__save_books_to_file()
        self.__save_readers_to_file()
        self.__save_history_to_file()
        print(f" Ksiazka wypozyczona.")

    def return_book(self, tytul, reader_id, date):
        if reader_id is None or tytul is None:
            print(f" Wszystkie dane (numer, tytul) musza być podane.")
            return
        if not re.match(r'^\d+$', str(reader_id)):
            print(f" ID musi być liczba.")
            return
        reader_id = int(reader_id)

        for reader in self.__readers:
            if reader.get_id() == reader_id:
                if tytul in reader.get_borrowed_books():
                    reader.remove_borrowed_book(tytul)
                    reader.increase_books_count()
                else:
                    print(f" Czytelnik nie ma wypozyczonej ksiazki o tytule {tytul}.")
                    return

        for book in self.__books:
            if book.get_tytul() == tytul and book.get_status() == "Wypozyczona":
                if datetime.strptime(book.get_borrow_history()[-1][1], "%d-%m-%Y %H:%M:%S") > datetime.\
                            strptime(date, "%d-%m-%Y %H:%M:%S"):
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
        with open('biblioteka.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Tytul", "autor", "Rok wydania", "Status"])
            for book in self.__books:
                writer.writerow([book.get_id(), book.get_tytul(), book.get_autor(), book.get_rok_wydania(),
                                 book.get_status()])

    def __save_history_to_file(self):
        with open('historia.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID ksiazki", "Numer czytacza", "Data wypozyczenia", "Data oddania"])
            for book in self.__books:
                for history in book.get_borrow_history():
                    writer.writerow([book.get_id(), history[0],
                                     history[1], history[2] if len(history) > 2 else "Nie zwrócono jeszcze"])

    def __save_readers_to_file(self):
        with open('czytacze.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Numer czytacza", "Imie", "Nazwisko", "Ilosc ksiazek"])
            for reader in self.__readers:
                writer.writerow([reader.get_id(), reader.get_name(), reader.get_surname(), reader.get_books_count()])

    def book_history(self, tytul):
        for book in self.__books:
            if book.get_tytul() == tytul:
                if book.get_borrow_history():
                    print(f"Historia wypozyczeń ksiazki {tytul}:")
                    for history in book.get_borrow_history():
                        print(f"Czytacz ID: {history[0]}, Data wypozyczenia: {history[1]}, Data zwrócenia:"
                              f" {history[2] if len(history) > 2 else 'Nie zwrócono jeszcze'}")
                else:
                    print(f"Ksiazka {tytul} nie byla jeszcze wypozyczona.")
                self.__save_history_to_file()  # add this line to save the history to file
                return
        print(f" Nie ma ksiazki o tytule {tytul}.")

    def __load_books_from_file(self):
        try:
            with open('biblioteka.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy naglówek
                for row in reader:
                    id_ksiazki, tytul, autor, rok_wydania, status = row
                    self.__books.append(Book(int(id_ksiazki), tytul, autor, int(rok_wydania), status))
        except FileNotFoundError:
            print(f" Brak pliku biblioteka.csv")

    def __load_history_from_file(self):
        try:
            with open('historia.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy naglówek
                for row in reader:
                    id_ksiazki, reader_id, borrow_date, return_date = row
                    try:
                        for book in self.__books:
                            if book.get_id() == int(id_ksiazki):
                                if return_date == "Nie zwrócono jeszcze":
                                    book.add_to_borrow_history(int(reader_id), borrow_date)
                                else:
                                    book.add_to_borrow_history(int(reader_id), borrow_date, return_date)
                                break
                    except ValueError:
                        print(f" W historii znaleziono nieprawidlowe ID czytelnika: {reader_id}")
        except FileNotFoundError:
            print(f" Brak pliku historia.csv")

    def __load_readers_from_file(self):
        try:
            with open('czytacze.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Pomijamy naglówek
                for row in reader:
                    reader_id, name, surname, books_count = row
                    self.__readers.append(Reader(int(reader_id), name, surname, int(books_count)))
        except FileNotFoundError:
            print(f" Brak pliku czytacze.csv")


def menu():
    library = Library()

    while True:
        print(f" MENU ")
        print(f"******************************")
        print("1. Dodaj ksiazkę")
        print("2. Wypozycz ksiazkę")
        print("3. Zwróć ksiazkę")
        print("4. Historia ksiazki")
        print("5. Wyjdź")
        print(f"******************************")

        option = input("Wybierz opcję: ")

        if option == "1":
            tytul = input("Podaj tytul ksiazki: ")
            autor = input("Podaj autora ksiazki: ")
            try:
                rok_wydania = int(input("Podaj rok wydania ksiazki: "))
                if rok_wydania > datetime.now().year or not str(rok_wydania).isdigit():
                    print(f" Rok wydania nie moze być większy niz {datetime.now().year}.")
                    continue
            except:
                print("Rokiem wydania musi być liczba.")
                continue
            library.add_book(tytul, autor, rok_wydania)

        elif option == "2":
            tytul = input("Podaj tytul ksiazki do wypozyczenia: ")
            reader_id = input("Wprowadź numer ID czytelnika: ")
            if not reader_id.isdigit():
                print(f" ID musi być liczba.")
                continue
            reader_id = int(reader_id)
            date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            library.lend_book(tytul, reader_id, date)

        elif option == "3":
            tytul = input("Podaj tytul lub ID ksiazki do zwrócenia: ")
            reader_id = input("Podaj numer lub ID czytelnika zwracajacego ksiazkę: ")
            if not reader_id.isdigit():
                print(f" ID musi być liczba.")
                continue
            reader_id = int(reader_id)
            date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            library.return_book(tytul, reader_id, date)

        elif option == "4":
            tytul = input("Podaj tytul ksiazki, której historię chcesz sprawdzić: ")
            library.book_history(tytul)

        elif option == "5":
            break
        else:
            print(f" Nieprawidlowa opcja. Sprobuj ponownie.")


if __name__ == "__main__":
    SanityCheck().check_files()
    menu()
