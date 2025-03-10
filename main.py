import os as system
import numpy as np


def wczytajWiadomosc(nazwaPliku):
    with open(nazwaPliku, "r", encoding="utf-8") as plik:
        plik = plik.read()
        plik = plik.strip()
        return plik


def napiszWiadomosc(nazwaPliku, wiadomosc):
    with open(nazwaPliku, "w", encoding="utf-8") as plik:
        plik.write(wiadomosc)


def sprawdzCzyIstnieje(nazwaPliku):
    # jesli istnieje
    if system.path.exists(nazwaPliku):
        zawartosc = wczytajWiadomosc(nazwaPliku)
        # i zawartosc nie jest pusta
        if len(zawartosc) != 0:
            # zwroc true
            return True
        else:
            print("Wiadomość jest pusta! Wybierz opcję 1 w menu głównym aby ją napisać.")
    else:
        print("Plik nie istnieje! Wybierz opcję 1 w menu głównym aby go utworzyć.")
    # plik nie istnieje lub jest pusty
    return False


def pobierzBityParzystosci(blok):
    # pomnoz kazdy blok (8 bitow) przez kazdy wiersz macierzy H i na koncu sumuj modulo 2

    # sformatuj blok tak, aby zawsze mial 8 bitow i byl binarny
    bityBloku = format(ord(blok), "08b")
    bityParzystosci = ""
    # dla wszystkich bitow w bloku (jest ich 8)
    for i in range(8):
        suma = 0
        # dla kazdej kolumny w macierzy H
        for j in range(8):
            # dodaj do sumy wartosc z macierzy pomnozonej razy wartosc calkowita z bitowBloku dla danej kolumny
            suma += H[i][j] * int(bityBloku[j])
        parzystosc = suma % 2
        bityParzystosci += str(parzystosc)
    return bityParzystosci


def zakodujWiadomosc(wiadomosc):
    # koduje wiadomosc, w petli dodaje bloki razem z bitami parzystosci obliczonymi na podstawie mac. H (8 + 8)
    wynik = ""
    for znak in wiadomosc:
        # pierwszy skladnik to dane w postaci binarnej (08b: zawsze 8 bitow),
        # drugi to bity parzystosci sprawdzajace poprawnosc
        wynik += format(ord(znak), "08b") + pobierzBityParzystosci(znak)
    return wynik


def odkodujWiadomosc(ciag):
    # odwraca proces jednoczesnie usuwajac bity parzystosci
    tekst = ""
    while ciag:
        # wez 16 znakow z ciagu
        blok = ciag[:16]
        # jesli jest mniej niz 16 bitow to zakoncz
        if len(blok) < 16:
            break
        dane = blok[:8]
        tekst += chr(int(dane, 2))
        ciag = ciag[16:]
    return tekst


def zweryfikujZnak(znakBin):
    # funkcja sprawdza czy jeden znak (blok) jest poprawny
    # R to zapisany ciag binarny znaku jako numpy array
    R = np.array(list(znakBin)).astype(int)
    # mnozymy R razy macierz H (funckja dot) i bierzemy mod 2
    HR = np.dot(H, R) % 2
    pozycje = []
    # w zakresie jednego bloku (16 bitow)
    for j in range(16):
        # iteruj po wszystkich kolumnach macierzy H
        # sprawdz dla kazdej kolumny, czy jest równa syndromowi błędu HR
        # jesli tak, to znaczy ze blad jest na pozycji "j"
        if np.array_equal(H[:, j], HR):
            # blad dodawany jest do slownika pozycje i opuszcza petle
            pozycje.append(j)
            break
    # wykrywanie podwojnych bledow
    # jesli nie znaleziono pojedynczego bledu (pusta lista pozycje)
    # sprawdzamy czy moga wystapic dwa bledy
    if not pozycje:
        # znowu iterujemy przez wszystkie kolumny macierzy H sumujemy ich modulow 2 i porownujemy
        for i in range(16):
            for j in range(i + 1, 16):
                sumaKolumn = (H[:, i] + H[:, j]) % 2
                # jesli suma dwoch kolumn jest rowna HR to znaczy za mamy podwojny blad
                if np.array_equal(sumaKolumn, HR):
                    pozycje.extend([i, j])
                    break
            if pozycje:
                break
    return pozycje


def zweryfikujWiadomosc(binarnyCiag):
    pozycjeBledow = []
    iteracja = 0
    while binarnyCiag:
        # dopoki mamy dalsze czesci binarnego ciagu danych
        blok = binarnyCiag[:16]
        # jesli dlugosc kolejnego bloku jest mniejsza niz 16 to przerwij
        if len(blok) < 16:
            break
        # uzyj funkcji i zapisz wyniki w liscie "bledy"
        bledy = zweryfikujZnak(blok)
        # zapisz wlasciwe pozycje bledow (wczesniej jest tylko dla jednego bloku dane 8bit i poprawnosc 8bit,
        # teraz jest bezwzgledna pozycja bledu
        for blad in bledy:
            bezwzglednaPozycja = iteracja * 16 + blad
            pozycjeBledow.append(bezwzglednaPozycja)
        # kontynuuj prace na dalszych blokach o ile istnieja
        binarnyCiag = binarnyCiag[16:]
        iteracja += 1
    return pozycjeBledow


# w macierzy H: brak zerowych kolumn, brak kolumn identycznych
# zeby korektowac podwojne bledy to zadna kolumna nie moze byc suma dwoch innych
H = np.array([[1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
              [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
              [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

niezakodowanaWiadomosc = "niezakodowanaWiadomosc.txt"
zakodowanaWiadomosc = "zakodowanaWiadomosc.txt"

print("Zadanie 1 - Kody wykrywające i korygujące błędy transmisji")
while True:
    print("--------------\nMenu Główne:\n"
          # 1. nadpisuje plik nowa wiadomoscia lub calkowicie tworzy nowy plik
          "1. Utwórz wiadomość do zakodowania\n"
          # 2. umozliwia uzytkownikowi sprawdzenie stanu zapisanej wiadomosci
          "2. Przygotowana wiadomość do zakodowania\n"
          # 3. koduje wiadomosc i zapisuje ja w osobnym pliku
          "3. Zakoduj wiadomość, zresetuj występujące błędy\n"
          # 4. odbiera wiadomosc, nastepnie sprawdza poprawnosc i jesli wystapil blad transmisji to poprawia
          "4. Odbierz zakodowaną wiadomość, zweryfikuj i popraw, jeśli wystąpiły błędy\n"
          # 5. powoduje opuszczenie programu
          "5. Zakończ program")
    wybor = input("Wybór: ")

    if wybor == "1":
        wiadomosc = input("Wprowadź komunikat: ")
        napiszWiadomosc(niezakodowanaWiadomosc, wiadomosc)
        input(f"Pomyślnie zapisano wiadomość do pliku \"{niezakodowanaWiadomosc}\".")
        print("Wybierz enter aby kontynuować.")

    elif wybor == "2":
        if sprawdzCzyIstnieje(niezakodowanaWiadomosc):
            print(wczytajWiadomosc(niezakodowanaWiadomosc))
        input("Wybierz enter aby kontynuować.")

    elif wybor == "3":
        if sprawdzCzyIstnieje(niezakodowanaWiadomosc):
            wiadomosc = wczytajWiadomosc(niezakodowanaWiadomosc)
            zakodowana = zakodujWiadomosc(wiadomosc)
            napiszWiadomosc(zakodowanaWiadomosc, zakodowana)
        input("Wybierz enter aby kontynuować.")

    elif wybor == "4":
        # odbierzIWeryfikujWiadomosc() nie dziala
        input("Wybierz enter aby kontynuować.")

    elif wybor == "5":
        print("Następuje opuszczenie programu.")
        break

    else:
        input("Wybrano niepoprawną opcję! Wybierz enter aby kontynuować.")
