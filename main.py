import os as system

def wczytajWiadomosc(nazwaPliku):
    with open(nazwaPliku, "r", encoding="utf-8") as plik:
        plik = plik.read().strip()
        return plik

def napiszWiadomosc(nazwaPliku, wiadomosc):
    with open(nazwaPliku, "w", encoding="utf-8") as plik:
        plik.write(wiadomosc)

def zakodujWiadomosc(wiadomosc):
    binarnaWiadomosc = ""
    for znak in wiadomosc:
        # ord(znak) - wez wartosc ASCII podanego znaku;
        # '08b' - oraz dolacz zera po prawej stronie tak, aby ciag mial 8 bitow
        binarnaWiadomosc += format(ord(znak), "08b")

    # na tym etapie wiadomosc to ciag 8-bitowych lancuchow: 8bit (spacja) 8bit (spacja) 8bit itd.
    zakodowana = ""
    for i in range(0, len(binarnaWiadomosc), 8):
        # dla kazdego 'bloku' majacego 8 bitow wykonuj
        # wez kolejny blok z ciagu (kolejne 8 bitow)
        blok = binarnaWiadomosc[i:i+8]
        # jesli jest mniej niz 8 bitow (nie powinno sie zdazyc ale moze)
        if len(blok) < 8:
            # to do bloku (np. 6) dodaj brakujace zera
            blok = blok + (8 - len(blok)) * "0"

        licznik = 0
        # sprawdz ile jest jedynek w bloku
        for bit in blok:
            if bit == "1":
                licznik += 1

        # jesli licznik jest parzysty (mod 2 daje 0) to nie dodawaj jedynki do bloku, bo juz jest parzysty
        if licznik % 2 == 0:
            dodajParzystosc = "0"
        else:
            # nieparzysta ilosc "1" w bloku: dodaj "1" aby bylo parzyscie
            dodajParzystosc = "1"

        # dodaj kolejny blok z bitem parzystosci do zakodowanego stringa
        zakodowana += blok + dodajParzystosc

    return zakodowana

def odkodujWiadomosc(wiadomosc):
    """Odkodowuje zakodowaną wiadomość. Usuwa bit parzystości z każdego bloku.
    Póki co (do zmiany) jeśli wykryta zostanie niezgodność parzystości to wyświetla info"""
    komunikat = ""
    for i in range(0, len(wiadomosc), 9):
        # dla kolejnych 9 znakow, zapisz konkretny blok
        blok = wiadomosc[i:i+9]
        if len(blok) < 9:
            # jesli blok nie jest pelny to zakoncz petle
            break
        # wez pierwsze 8 znakow (to sa dane)
        dane = blok[0:8]
        # zapisz ostatni znak jako znak parzystosci (1 dopelnia do parzystosci, 0 mowi ze dane sa parzyste)
        parzystosc = blok[8]
        # sprawdzamy czy sie parzystosc zgadza
        licznikJedynek = dane.count("1")
        if licznikJedynek % 2 == 0:
            realnaParzystosc = "0"
        else:
            realnaParzystosc = "1"

        # jesli parzystosc sie nie zgadza to wysweitl blad
        if parzystosc != realnaParzystosc:
            print(f"Wykryto błąd w bloku '{i}': niezgodność parzystości")

        # Przekonwertuj dane binarne na znak ASCII
        # zamien bin na dec
        wartoscDziesietna = int(dane, 2)
        # zamien dec na ascii
        blokZnakow = chr(wartoscDziesietna)
        # dodaj blok odkodowanych znakow do komunikatu
        komunikat += blokZnakow
    return komunikat

# main
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
        nazwaPliku = "niezakodowanaWiadomosc.txt"
        wiadomosc = input("Wprowadź komunikat: ")
        napiszWiadomosc(nazwaPliku, wiadomosc)
        input(f"Pomyślnie zapisano wiadomość do pliku \"{nazwaPliku}\".\n"
              f"Wybierz enter aby kontynuować.")

    elif wybor == "2":
        print("todo")

    elif wybor == "3":
        print("todo")

    elif wybor == "4":
        print("todo")

    elif wybor == "5":
        print("todo")
        # exit(0) ? moze jeszcze upewnic sie czy zasoby sa zamkniete

    else:
        input("Wybrano niepoprawną opcję! Wybierz enter aby kontynuować.")