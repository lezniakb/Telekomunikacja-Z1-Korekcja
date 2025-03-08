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