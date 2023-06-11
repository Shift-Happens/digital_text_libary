import csv
import random
import os
from datetime import datetime, date


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
BIBLIOTEKA_PLIK_CSV = "biblioteka.csv"
CZYTELNICY_PLIK_CSV = "czytacze.csv"
HISTORIA_PLIK_CSV = "historia.csv"


class Ksiazka:
    def __init__(self, id_ksiazki, tytul, autor, rok_wydania_ksiazki, status):
        self.numer_czytelnika = None
        self.id = int(id_ksiazki)
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = int(rok_wydania_ksiazki)
        self.status = status

    def czy_jest_dostepna(self):
        return self.status == STATUS_KSIAZKI_W_BIBLIOTECE

    def oznacz_jako_dostepna(self):
        self.status = STATUS_KSIAZKI_W_BIBLIOTECE
        self.numer_czytelnika = None

    def oznacz_jako_wypozyczona(self, numer_czytelnika):
        self.status = "Wypozyczona"
        self.numer_czytelnika = numer_czytelnika


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


class TyTylkoTuIstniejeszZebyMocPrzerwacPetle:
    def __init__(self, message):
        self.message = message
    pass

    message = "TyTylkoTuIstniejeszZebyMocPrzerwacPetle zadziałalo"


class Biblioteka:
    def __init__(self):
        self.cytaty = None
        self.ksiazki = []
        self.czytelnicy = []
        self.historia = []

    def wybor_operacji(self):
        self.wczytanie_z_pliku_csv()
        while True:
            self.text_menu()
            wybor = self.weryfikacja_czy_liczba("Wybierz opcje: ")
            if wybor == 1:
                self.__dodaj_ksiazke()
            elif wybor == 2:
                self.__wypozycz_ksiazke()
            elif wybor == 3:
                self.__oddaj_ksiazke()
            elif wybor == 4:
                self.__sprawdz_historie_ksiazki()
            elif wybor == 5:
                self.zapisanie_do_pliku_csv()
                break
            else:
                print("Opcja która została wybrana nie istnieje")

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
            3: "Można, ależ oczywiście, że tak. Nawet trzeba",
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
            14: "Róbcie dzieci ale nie róbcie dzieci",
            15: "chatGPT jest słaby więc nie użyłem go do pisania tych cytatów"
        }
        return self.cytaty[los]

    def __dodaj_ksiazke(self):
        tytul = self.weryfikacja_czy_polskie_znaki("Podaj tytuł: ")
        autor = self.weryfikacja_czy_polskie_znaki("Podaj autora: ")
        rok = self.weryfikacja_czy_liczba("Podaj rok wydania: ")
        id_ksiazki = len(self.ksiazki) + 1
        ksiazka = Ksiazka(id_ksiazki, tytul, autor, rok, STATUS_KSIAZKI_W_BIBLIOTECE)
        self.ksiazki.append(ksiazka)
        print("Dodano ksiazke do biblioteki.")

    def __wypozycz_ksiazke(self):
        while True:
            oznaczenie_ksiazki = self.weryfikacja_czy_polskie_znaki("Podaj numer indeksu lub tytuł książki: ")
            numer_czytelnika = self.weryfikacja_czy_liczba("Podaj numer czytelnika: ")
            imie = self.weryfikacja_czy_polskie_znaki("Podaj imię: ")
            nazwisko = self.weryfikacja_czy_polskie_znaki("Podaj nazwisko: ")
            czytelnik = self.__znajdz_czytelnika(numer_czytelnika)
            if not self.__zweryfikuj_czytelnika(numer_czytelnika, imie, nazwisko):
                continue
            if not czytelnik:
                czytelnik = Czytelnik(numer_czytelnika, imie, nazwisko, 0)
                self.czytelnicy.append(czytelnik)
            try:
                ksiazka = self.__znajdz_ksiazke(oznaczenie_ksiazki, True)
                if not ksiazka.czy_jest_dostepna():
                    print("Książka jest już wypożyczona")
                    raise TyTylkoTuIstniejeszZebyMocPrzerwacPetle
                data = self.__sprawdz_i_pobierz_date(ksiazka.id, True)
            except TyTylkoTuIstniejeszZebyMocPrzerwacPetle:
                self.__dodaj_niepowodzenie_do_historii(czytelnik.numer_czytelnika)
                break
            ksiazka.oznacz_jako_wypozyczona(czytelnik.numer_czytelnika)
            czytelnik.dodaj_ksiazke()
            self.__dodaj_sukces_do_historii(ksiazka.id, czytelnik.numer_czytelnika, data, None)
            print("Wypożyczono książkę")
            break

    def __oddaj_ksiazke(self):
        while True:
            oznaczenie_ksiazki = self.weryfikacja_czy_polskie_znaki("Podaj numer indeksu lub tytuł książki: ")
            try:
                ksiazka = self.__znajdz_ksiazke(oznaczenie_ksiazki, False)
                if ksiazka.numer_czytelnika is None:
                    print("Książka nie jest wypożyczona")
                    raise TyTylkoTuIstniejeszZebyMocPrzerwacPetle
                data = self.__sprawdz_i_pobierz_date(ksiazka.id, False)
            except TyTylkoTuIstniejeszZebyMocPrzerwacPetle:
                self.__dodaj_niepowodzenie_do_historii(ksiazka.numer_czytelnika)
                break
            czytelnik = self.__znajdz_czytelnika(ksiazka.numer_czytelnika)
            if not czytelnik:
                print("Nie znaleziono czytacza")
                continue
            self.__dodaj_sukces_do_historii(
                ksiazka.id, czytelnik.numer_czytelnika, None, data
            )
            ksiazka.oznacz_jako_dostepna()
            czytelnik.odejmij_ksiazke()
            print("Książka została zwrócona do biblioteki")
            break

    # todo: napisać funkcje sprawdz_historie_ksiazki
    def __sprawdz_historie_ksiazki(self):
        while True:
            oznaczenie_ksiazki = self.weryfikacja_czy_polskie_znaki("Podaj numer indeksu lub tytuł książki: ")
            try:
                ksiazka = self.__znajdz_ksiazke(oznaczenie_ksiazki, False)
            except TyTylkoTuIstniejeszZebyMocPrzerwacPetle:
                break
            czy_jest_ksiazka_w_historii = False
            for zdarzenie in self.historia:
                if zdarzenie.id_ksiazki == ksiazka.id:
                    czy_jest_ksiazka_w_historii = True
                    print(zdarzenie)
            if not czy_jest_ksiazka_w_historii:
                print("Dla podanej książki nie ma historii.")
            if ksiazka.czy_jest_dostepna():
                print("Książka została znaleziona w bibliotece")
            else:
                print("Książka została wypożyczona")
            break

    # todo: zmienic nazwe
    def __dodaj_sukces_do_historii(self, id_ksiazki, numer_czytelnika, data_wypozyczenia, data_zwrotu):
        # Sprawdź, czy istnieje zdarzenie w historii, które spełnia warunki
        for zdarzenie in self.historia:
            if zdarzenie.id_ksiazki == id_ksiazki and zdarzenie.numer_czytelnika == numer_czytelnika and \
                    zdarzenie.czy_sie_udalo == "Tak" and \
                    (zdarzenie.data_wypozyczenia is None or zdarzenie.data_zwrotu is None):
                # Aktualizuj datę wypożyczenia, jeśli jest None
                if zdarzenie.data_wypozyczenia is None:
                    zdarzenie.data_wypozyczenia = data_wypozyczenia
                # Aktualizuj datę zwrotu, jeśli jest None
                if zdarzenie.data_zwrotu is None:
                    zdarzenie.data_zwrotu = data_zwrotu
                break
        else:
            # Dodaj nowe zdarzenie do historii
            self.historia.append(
                Wydarzenia(id_ksiazki, numer_czytelnika, "Tak", data_wypozyczenia, data_zwrotu)
            )

    def __dodaj_niepowodzenie_do_historii(self, numer_czytelnika):
        self.historia.append(
            Wydarzenia(None, numer_czytelnika, "Nie", None, None)
        )

    def __waliduj_date_historia(self, data, id_ksiazki, czy_wypozycza):
        ostatnia_data_wypozyczenia = None
        ostatnia_data_oddania = None

        for zdarzenie in sorted(
                self.historia,
                key=lambda e: e.data_wypozyczenia
                if e.data_wypozyczenia is not None
                else date.max,
                reverse=True,
        ):
            if zdarzenie.id_ksiazki == id_ksiazki:
                if zdarzenie.data_wypozyczenia:
                    ostatnia_data_wypozyczenia = zdarzenie.data_wypozyczenia
                if zdarzenie.data_zwrotu:
                    ostatnia_data_oddania = zdarzenie.data_zwrotu
                break

        if czy_wypozycza:
            if ostatnia_data_wypozyczenia and not ostatnia_data_oddania:
                print("Książka jest obecnie wypożyczona.")
                raise TyTylkoTuIstniejeszZebyMocPrzerwacPetle

            if ostatnia_data_oddania and data < ostatnia_data_oddania:
                print(
                    "Data wypożyczenia nie może być wcześniejsza niż data ostatniego oddania."
                )
                return False
        else:
            if not ostatnia_data_wypozyczenia or ostatnia_data_oddania:
                print("Nie można zwrócić książki, która nie jest wypożyczona.")
                raise TyTylkoTuIstniejeszZebyMocPrzerwacPetle

            if data < ostatnia_data_wypozyczenia:
                print("Data oddania nie może być wcześniejsza niż data wypożyczenia.")
                return False

        return True

    def __sprawdz_date_rok_wydania(self, data, id_ksiazki):
        ksiazka = next((k for k in self.ksiazki if k.id == id_ksiazki), None)
        if ksiazka is None:
            print("Nie znaleziono książki.")
            return False
        if data < date(ksiazka.rok_wydania, 1, 1):
            print("Data nie może być wcześniejsza niż rok wydania książki.")
            return False
        return True

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

    @staticmethod
    def wartosc_pusta(wartosc):
        if wartosc == "":
            return None
        else:
            return wartosc

    def zapisanie_do_pliku_csv(self):
        dane_plikow = [
            {"nazwa_pliku": BIBLIOTEKA_PLIK_CSV,
             "header": ["ID", "Tytul", "Autor", "Rok wydania", "Status"],
             "tablica": self.ksiazki,
             "funkcja": lambda ksiazka: [
                 ksiazka.id,
                 ksiazka.tytul,
                 ksiazka.autor,
                 ksiazka.rok_wydania,
                 ksiazka.status, ],
             },
            {"nazwa_pliku": CZYTELNICY_PLIK_CSV,
             "header": ["Numer czytacza", "Imie", "Nazwisko", "Ilosc ksiazek"],
             "tablica": self.czytelnicy,
             "funkcja": lambda czytacz: [
                 czytacz.numer_czytelnika,
                 czytacz.imie,
                 czytacz.nazwisko,
                 czytacz.ilosc_ksiazek, ],
             },
            {"nazwa_pliku": HISTORIA_PLIK_CSV,
             "header": [
                 "ID",
                 "Numer czytacza",
                 "Czy udana",
                 "Data wypozyczenia",
                 "Data zwrotu",
             ],
             "tablica": self.historia,
             "funkcja": lambda zdarzenie: [
                 zdarzenie.id_ksiazki,
                 zdarzenie.numer_czytelnika,
                 zdarzenie.czy_sukces,
                 zdarzenie.data_wypozyczenia,
                 zdarzenie.data_oddania, ],
             },
        ]

        for dane_pliku in dane_plikow:
            with open(dane_pliku["nazwa_pliku"], "w", newline="") as plik:
                writer = csv.writer(plik)
                writer.writerow(dane_pliku["header"])
                writer.writerows(map(dane_pliku["funkcja"], dane_pliku["tablica"]))

    def wczytanie_z_pliku_csv(self):
        dane_plikow = [
            {
                "nazwa_pliku": BIBLIOTEKA_PLIK_CSV,
                "funkcja": lambda wiersz: Ksiazka(
                    *[self.wartosc_pusta(val) for val in wiersz]
                ),
                "dodaj_do": self.ksiazki,
                "etykieta": "ID",
            },
            {
                "nazwa_pliku": CZYTELNICY_PLIK_CSV,
                "funkcja": lambda wiersz: Czytelnik(
                    *[self.wartosc_pusta(val) for val in wiersz]
                ),
                "dodaj_do": self.czytelnicy,
                "etykieta": "Numer czytacza",
            },
            {
                "nazwa_pliku": HISTORIA_PLIK_CSV,
                "funkcja": lambda wiersz: Wydarzenia(
                    *[self.wartosc_pusta(val) for val in wiersz]
                ),
                "dodaj_do": self.historia,
                "etykieta": "ID",
            },
        ]

        for dane_pliku in dane_plikow:
            if os.path.exists(dane_pliku["nazwa_pliku"]):
                with open(dane_pliku["nazwa_pliku"], "r") as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip the header row
                    for row in reader:
                        if row and row[0] != dane_pliku["etykieta"]:
                            item = dane_pliku["funkcja"](row)
                            dane_pliku["dodaj_do"].append(item)

    def __znajdz_czytelnika(self, numer_czytelnika):
        return next(
            (czytelnik for czytelnik in self.czytelnicy if czytelnik.numer_czytelnika == numer_czytelnika), None)

    def __znajdz_ksiazke(self, oznaczenie_ksiazki, czy_wypozycza):
        znalezione_ksiazki = []
        for ksiazka in self.ksiazki:
            if str(ksiazka.id) == oznaczenie_ksiazki or ksiazka.tytul == oznaczenie_ksiazki:
                znalezione_ksiazki.append(ksiazka)
        if not znalezione_ksiazki:
            print("Nie znaleziono książki o podanym oznaczeniu")
            return False
        znalezione_ksiazki.sort(key=lambda znaleziona_ksiazka: znaleziona_ksiazka.id)
        if len(znalezione_ksiazki) == 1 or czy_wypozycza:
            return znalezione_ksiazki[0]
        indeks = self.weryfikacja_czy_liczba(
            "Znaleziono kilka książek o podanym tytule, proszę podać numer indeksu: "
        )
        return self.__znajdz_ksiazke(indeks, False)

    def __zweryfikuj_czytelnika(self, numer_czytelnika, imie, nazwisko):
        czytelnik = self.__znajdz_czytelnika(numer_czytelnika)
        if czytelnik is not None:
            print("Czytelnik o podanym numerze już istnieje. Proszę podać inny numer.")
            return False

        for czytelnik in self.czytelnicy:
            if czytelnik.imie == imie:
                print("Czytelnik o podanym imieniu już istnieje. Proszę podać inne imię.")
                return False
            if czytelnik.nazwisko == nazwisko:
                print(
                    "Czytelnik o podanym nazwisku już istnieje. Proszę podać inne nazwisko."
                )
                return False
        return True

    def __sprawdz_i_pobierz_date(self, id_ksiazki, czy_wypozycza):
        while True:
            data = self.__pobierz_date()
            if not self.__sprawdz_date_rok_wydania(data, id_ksiazki):
                continue
            try:
                if not self.__waliduj_date_historia(data, id_ksiazki, czy_wypozycza):
                    continue
            except TyTylkoTuIstniejeszZebyMocPrzerwacPetle:
                break
            return data

    def __pobierz_date(self):
        while True:
            data_str = self.weryfikacja_czy_polskie_znaki("Podaj datę (dd/mm/rrrr): ")
            try:
                data = datetime.strptime(data_str, "%d/%m/%Y").date()
                return data
            except ValueError:
                print("Niepoprawny format daty. Proszę spróbować ponownie.")


class Wydarzenia:
    def __init__(self, id_ksiazki, numer_czytelnika, czy_udana, data_wypozyczenia=None, data_oddania=None):
        self.id_ksiazki = None if id_ksiazki is None else int(id_ksiazki)
        self.numer_czytelnika = int(numer_czytelnika)
        self.czy_sie_udalo = czy_udana
        self.data_wypozyczenia = data_wypozyczenia
        self.data_oddania = data_oddania

    def __str__(self):
        return f"ID Ksiazki{self.id_ksiazki}, Numer czytacza: {self.numer_czytelnika}, Czy udana:{self.czy_sie_udalo}" \
               f",Data Wypozyczenia{self.data_wypozyczenia}, Data oddania: {self.data_oddania} "


def main():
    Biblioteka().wybor_operacji()


if __name__ == "__main__":
    SanityCheck().check_files()
    main()
