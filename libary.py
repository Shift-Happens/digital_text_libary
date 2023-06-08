import csv
import random


# from datetime import datetime
# from unidecode import unidecode
# import re


class SanityCheck:
    def __init__(self):
        self.check_files()

    @staticmethod
    def check_files():
        try:
            with open("biblioteka.csv", "r"):
                pass
        except FileNotFoundError:
            with open("biblioteka.csv", "w", newline="") as books_file:
                books_writer = csv.writer(books_file, delimiter=",")
                books_writer.writerow(["ID", "Tytul", "autor", "Rok wydania", "Status"])

        try:
            with open("czytacze.csv", "r"):
                pass
        except FileNotFoundError:
            with open("czytacze.csv", "w", newline="") as readers_file:
                readers_writer = csv.writer(readers_file, delimiter=",")
                readers_writer.writerow(["Numer czytacza", "Imie", "Nazwisko", "Ilosc ksiazek"])

        try:
            with open("historia.csv", "r"):
                pass
        except FileNotFoundError:
            with open("historia.csv", "w", newline="") as history_file:
                history_writer = csv.writer(history_file, delimiter=",")
                history_writer.writerow(["ID", "Numer czytacza", "Czy udana", "Data wypozyczenia", "Data oddania"])


STATUS_KSIAZKI_W_BIBLIOTECE = "W bibliotece"


class Ksiazka:
    def __init__(self, id_ksiazki, tytul, autor, rok_wydania_ksiazki, status):
        self.id = int(id_ksiazki)
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = int(rok_wydania_ksiazki)
        self.status = status

    def czy_jest_dostepna(self):
        return self.status == STATUS_KSIAZKI_W_BIBLIOTECE


class Czytelnik:
    def __init__(self, numer_czytelnika, imie, nazwisko, ilosc_ksiazek):
        self.numer_czytelnika = int(numer_czytelnika)
        self.imie = imie
        self.nazwisko = nazwisko
        self.ilosc_ksiazek = int(ilosc_ksiazek)

    def dodaj_ksiazke(self):
        self.ilosc_ksiazek += 1

    def odejmij_ksiazke(self):
        self.ilosc_ksiazek -= 1


class Biblioteka:
    def __init__(self):
        self.cytaty = None
        self.ksiazki = []
        self.czytelnicy = []
        self.historia = []

    def wybor_operacji(self):
        # trzeba zrobic funkcje ktra zaladuje pliki i bedzie na nich operowac
        # zostanie wywoana tutaj przed odpaleniem menu  i po zakonczeniu programu
        # do menu uyje petli while True ze slownikiem wyboru opcji
        self.text_menu()  # wyswietla menu - mozna latwo dodac nowe opcje bez ingerencji w kod
        wybor = self.weryfikacja_czy_liczba("Wybierz opcje: ")
        while True:
            menu = {
                1: self.__dodaj_ksiazke,
                2: self.__wypozycz_ksiazke,
                3: self.__oddaj_ksiazke,
                4: self.__sprawdz_historie_ksiazki,
                5: self.__zakoncz_program
            }

            if wybor in menu:
                menu[wybor]()
            else:
                print("Opcja która została wybrana nie istnieje")
            if wybor == 5:
                break

    def text_menu(self):
        print(f"""
Menu:
Inspiracyny quote instancji wczytania menu: {self.quote_dnia()}
*********************************
1. Dodaj książkę
2. Wypożycz książkę
3. Oddaj książkę
4. Sprawdź historię książki
5. Zakończ program
*********************************""")

    def quote_dnia(self):
        los = random.randint(1, 15)
        self.cytaty = {
            1: "Czytanie książek to najpiękniejsza zabawa, tak samo jak jedzenie kebaba.",
            2: "Jeśli coś jest głupie, ale działa, to nie jest głupie, albo jest bardzo głupie, ale działa.",
            3: "Można, ależ oczywiście, żw tak. Nawet trzeba",
            4: "Nić dentystyczna jest dobra na wszystko",
            5: "Sól do kąpieli jest przeznaczona do kąpieli, a nie do jedzenia",
            6: "Sraken jest najlepszym smokiem",
            7: "Fireball w DnD jest przereklamowany",
            8: "Freddy Mercury był gejem",
            9: "Michael Jackson robił hajsy na dzieciach",
            10: "Hitler był dobrym malarzem",
            11: "Tworzenie własnej dystrybucji Linuxa nie jest dobrym pomysłem",
            12: "TechWithTim robi dobre tutoriale na YT",
            13: "Książki w Empiku są turbo drogie",
            14: "Evviva L'arte",
            15: "chatGPT jest słaby więc nie użyłem go do pisania tych cytatów"
        }
        return self.cytaty[los]

    # todo: napisać funkcje dodaj_ksiazke
    def __dodaj_ksiazke(self):
        pass

    # todo: napisać funkcje wypozycz_ksiazke
    def __wypozycz_ksiazke(self):
        pass

    # todo: napisać funkcje oddaj_ksiazke
    def __oddaj_ksiazke(self):
        pass

    # todo: napisać funkcje sprawdz_historie_ksiazki
    def __sprawdz_historie_ksiazki(self):
        pass

    # todo: funkcja ktrra ma zapisac wydarzenie do historii, jak i jego status
    @staticmethod
    def __wydarzenie_do_historii():
        pass

        def sukces():
            pass

        def porazka():
            pass

    # todo: napisać funkcje zakoncz_program
    def __zakoncz_program(self):
        # zapisuje wszystkie pliki i konczy program
        pass

    @staticmethod
    def weryfikacja_czy_liczba(tekst):
        while True:
            try:
                wybor = int(input(tekst))
                return wybor
            except ValueError:
                print("Wprowadź liczbę! Podana wartosc nie jest liczba :c")

    @staticmethod
    def weryfikacja_czy_polskie_znaki(tekst):
        polskie_znaki = ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż"]
        while True:
            wyrazenie = input(tekst.lower())
            for znak in wyrazenie:
                if znak in polskie_znaki:
                    print("Nie wprowadzaj polskich znaków!")
                    break
                else:
                    return wyrazenie

    # todo: napisać funkcje która sprawdzi czy wartość jest pusta i zwróci None albo wartość
    def wartosc_pusta(self, wartosc):
        pass

    # todo: funkcja która wprowadzi parfametry i dane do plików csv
    def zapisanie_do_pliku_csv(self):
        pass

    # todo: funkcja która wczyta dane z plików csv
    def wczytanie_z_pliku_csv(self):
        pass


# todo napisać klase która doda eventy do historii
class Wydarzenia:
    def __init__(self):
        self.id = 0
        self.numer_czytelnika = 0
        self.czy_udana = False
        self.data_wypozyczenia = None
        self.data_oddania = None

    # todo: funkcja która będzie zwracać stringa żeby można było go łatwo zaimplemetować w różnych miejscach
    def __str__(self):
        return f"{self.id}, Numer czytacza: {self.numer_czytelnika}, Czy udana:{self.czy_udana}, " \
               f"Data Wypozyczenia{self.data_wypozyczenia}, Data oddania: {self.data_oddania} "


def main():
    biblioteka = Biblioteka()
    biblioteka.wybor_operacji()


if __name__ == "__main__":
    SanityCheck().check_files()
    main()
