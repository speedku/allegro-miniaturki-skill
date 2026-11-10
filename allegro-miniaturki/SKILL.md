---
name: allegro-miniaturki
description: "Use when the user asks for an Allegro offer thumbnail (first photo of the offer) or extra gallery photos generated with AI: zrób miniaturkę na Allegro, miniaturka z kartonem, miniaturka z opakowaniem, dorób zdjęcia do oferty, więcej grafik do tego produktu na Allegro, or gives only an allegro.pl/oferta link. Produces thumbnails that follow the Allegro image rules: pure white background, no shadows, no added text, no watermark, whole product in frame."
---

# Miniaturki ofert Allegro z generatora AI

Cel: pierwsze zdjęcie oferty (miniaturka), które pokazuje **realny towar** i przechodzi wymagania
Allegro dla zdjęć, oraz ewentualne sceny do galerii. Skill opisuje proces i reguły, a nie konkretny
generator: działa z każdym narzędziem, które przyjmuje prompt i zdjęcie referencyjne (img2img).

## 1. Twarde wymagania miniaturki (pierwsze zdjęcie oferty)

| Wymaganie | Jak sprawdzasz |
|---|---|
| Tło czysto białe #FFFFFF, bez gradientu, winiety i ramki | `scripts/bramka-tla.py` |
| Zero cieni, także kontaktowego pod produktem, zero odbić podłoża | `scripts/bramka-tla.py` i oko |
| Zero dodanych napisów i grafik: wymiary, linie miarowe, plakietki, ramki, ulotki, karty z tekstem | powiększenie kadru |
| Zero znaku wodnego i znaku "AI" w rogu, zero logo sprzedawcy | mozaika rogów |
| Produkt w całości w kadrze, biały margines min. 4-5 % z każdej strony, nic nie dotyka krawędzi | `scripts/biale-tlo.py` (linia `PRZYCIETE`) |
| Produkt zajmuje większość kadru | oko |
| Kwadrat, docelowo 2000x2000 px, JPG | rozmiar pliku |
| Towar taki sam jak w rzeczywistości: kolor, kształt, liczba elementów | porównanie z referencją |

Nadruk, który jest częścią produktu albo jego opakowania (napis na torbie, etykieta na butelce),
zostaje i ma być wierny. Zakaz dotyczy tego, co dodane do zdjęcia.

Sceny aranżacyjne w dalszej części galerii mogą mieć cienie, tło i rekwizyty. Zakaz obcych logo
obowiązuje wszędzie.

Zestaw albo pakiet: miniaturka to packshot **całego** zestawu na białym tle, bez rekwizytów.

## 2. Przebieg

1. **Dane oferty.** Tytuł mówi, co ma być na kadrze (pojemność, typ, liczba sztuk). Strona
   `allegro.pl/oferta/...` odpowiada skryptom kodem 403, więc czytaj ją w przeglądarce albo przez API Allegro.
2. **Co oferta ma dzisiaj.** Obejrzyj obecną galerię, żeby nie dorobić kopii istniejących zdjęć.
3. **Referencja produktu (obowiązkowa).** Bez zdjęcia referencyjnego model wymyśla własny towar.
   Weź zdjęcie produktu na białym tle, bez cudzego pudełka (zwykle 2. albo 3. zdjęcie galerii).
   Jeśli na referencji jest znak "AI" albo plakietka, odetnij ten pas przed wysłaniem.
4. **Prompt** (sekcja 3) i generacja: zawsze kilka wariantów jednego kadru.
5. **Obróbka:** tylko dobielenie tła (`biale-tlo.py`) i usunięcie plakietki generatora. Nic się nie dokleja.
6. **Odbiór** (sekcja 6): każdy kadr oglądasz w powiększeniu i puszczasz przez bramkę.
7. **Oddanie plików.** Zdjęć nie wgrywasz na ofertę samodzielnie: zmiana żywej oferty wymaga wyraźnej prośby.

## 3. Prompt

Stały ogon, dopisywany do każdego promptu:

```
<Produkt> DOKŁADNIE jak na referencji: <kolor i materiał>, <kolor oprawy>. Nie zmieniaj
i nie nasycaj kolorów. Realistyczne i naturalne, kadr kwadratowy, cały produkt w kadrze,
nieprzycięty. Najwyższa jakość. Bez tekstu i bez obcych logo.
```

Dla miniaturki dodatkowo:

```
pure white background #FFFFFF, no shadow, no reflection, szeroki biały margines dookoła
```

Zasady:

- **Długość.** Cały prompt poniżej ok. 500 znaków, opis sceny ok. 130. Długie prompty z referencją częściej kończą się błędem albo zgubieniem referencji.
- **Kolor słownie.** Samo zdjęcie bywa za słabym sygnałem. Przy jasnym towarze model podbija odcień: dopisz "BLADY" i "odcień ma być jasny, nie ciemniejszy".
- **Makro to nie przycięcie.** Przy zbliżeniach pisz "wszystkie przedmioty W CAŁOŚCI w kadrze z marginesem".
- **Liczba elementów wprost.** "DOKŁADNIE PIĘĆ haczyków, ani jednego mniej". Model gubi i dokłada elementy.
- **Długie, miękkie rzeczy uciekają za kadr** (wstążki, sznurki, taśmy): "CAŁY w kadrze, kończy się daleko przed krawędzią".
- **Bez śmieci:** "ŻADNYCH dodatkowych ulotek, karteczek ani etykiet w kadrze".
- **"Wizualizacja produktowa"** albo "katalogowa" zamiast samego "packshot": wychodzi bardziej fotograficznie.
- **Kilka referencji:** nazwij rolę każdej: "układ jak na PIERWSZEJ", "produkt jak na DRUGIEJ", "nadruk DOKŁADNIE jak na TRZECIEJ".

Kadr niezgodny z realnym towarem jest błędem tej samej wagi co obca marka: klient dostaje co innego, niż widzi.

## 4. Miniaturka z opakowaniem (z kartonem)

Prośba "miniaturka z kartonem / z opakowaniem" oznacza **kilkanaście propozycji różnych opakowań**, nie jedno pudełko w wielu ujęciach.

1. Dobierz 3-4 typy opakowania pasujące do produktu i zrób jedną partię 12-16 kadrów (po 3-4 na typ).
   Pomysły: karton handlowy, pudełko z okienkiem, tuba PET, banderola z zawieszką, blister z eurozawieszką,
   puszka, woreczek z oknem, pudełko prezentowe. Zapytaj siebie, jak ten towar sprzedaje sklep branżowy.
2. Nie wszystko w szarym krafcie. Opakowanie dobierasz do charakteru towaru, a pudełka w serii mają się od siebie różnić.
3. Pokaż propozycje na jednej planszy z literami A, B, C..., wybrany kierunek dopracuj drugą rundą.

Układ, który działa:

- **Produkt na pierwszym planie i duży, opakowanie w głębi**, lekko pod kątem. Karton nie może dominować.
- **Skala zgodna z rzeczywistością:** produkt nie może wyglądać na większy od własnego opakowania.
- **Bryły wyraźnie oddzielone**, między nimi pas białego tła. Gdy na froncie kartonu jest zdjęcie tego samego
  produktu, dwie sylwetki zlewają się w jedną: odsuń karton, obróć go bokiem albo postaw w rogu kadru.
- **Klient musi zobaczyć sam towar**, nie tylko opakowanie (przy materiałach: rozwinięty pas albo kokarda z ostrą fakturą).
- **Szkło i naczynia:** produkt z przodu, kartonik z tyłu. Szkło przed kartonem nie może wyjść białe w środku.

Referencja opakowania:

- Najlepsza jest **fotografia realnego kartonu** zrobiona telefonem. Płaski render daje płaskie, rozpłaszczone pudełko.
- Przycinając referencję, nigdy nie skaluj do sztywnego rozmiaru: zachowaj proporcje i porównaj je z realnym pudełkiem.
- Gdy kartonu jeszcze nie ma, referencją może być narysowany panel frontu, a bryłę robi model.
- Etykietę z danymi narysuj sam (ostry tekst) i podaj jako osobną referencję.
- Przed wysłaniem obejrzyj referencję: dane dostawcy, numery zamówień i cudze kody EAN nie mogą trafić do modelu.

**Finalny kadr powstaje w całości w generatorze.** Zakaz nakładania zdjęcia kartonu, panelu, ścianki albo napisu
na wygenerowany obraz, także "tylko boku". Gdy drobny druk wychodzi przekręcony, zrób kolejną rundę z innym
układem i mniejszą ilością drobnego tekstu, a przy oddaniu napisz wprost, co odbiega.

Uwaga na regułę z sekcji 1: nadruk na opakowaniu to nadruk produktu, ale osobne karty, wymiary
i plakietki już nie.

## 5. Sceny do galerii (opcjonalnie)

Sprawdzony zestaw 8 kwadratowych kadrów dla produktu użytkowego:

| # | Kadr | Po co |
|---|---|---|
| 1 | packshot pełnego zestawu na białym tle | miniaturka, klient widzi ile sztuk dostaje |
| 2 | makro pojedynczej sztuki | detal i parametry z etykiety |
| 3-7 | sceny użycia w różnych kontekstach | pokazuje, do czego to pasuje |
| 8 | zapas w szufladzie albo stos opakowań | uzasadnia zakup większej paczki |

Wzór promptu sceny:

```
Realistyczne zdjęcie: <kto co robi z produktem>, <miejsce>, obok <opakowanie> z referencji.
<Światło>, kadr kwadratowy, płytka głębia ostrości. <Produkt> DOKŁADNIE jak na zdjęciu
referencyjnym. Bez dodatkowego tekstu i bez obcego logo.
```

## 6. Obróbka i odbiór

```bash
pip install numpy opencv-python pillow
python scripts/biale-tlo.py  <wejście.jpg> <wyjście.jpg>   # tło do #FFFFFF + pomiar marginesu
python scripts/bramka-tla.py <plik.jpg> [...]              # siatka 24x24, zero cieni; kod wyjścia 1 = odrzut
```

- `biale-tlo.py` wypisuje margines. `PRZYCIETE` = kadr do kosza, `CIASNO` = do oceny.
- **Bielenie nie zastępuje nowej generacji.** Cień, smugi albo halo po bieleniu: generuj od nowa.
- Bramka nie odróżnia białego produktu od szarego tła. Przy białych i przezroczystych produktach rozstrzyga oko.
- Plakietkę generatora w rogu zamaluj wąskim prostokątem z pasa tuż obok. Nie odcinaj kadru: produkt bywa 30 px od krawędzi.
  Najpierw sprawdź, w którym rogu plakietka siedzi, generatory to zmieniają.

Kolejność odbioru każdego kadru:

1. liczba elementów w powiększeniu (na pełnym kadrze różnica cztery kontra pięć jest niewidoczna),
2. kolor i kształt względem referencji,
3. napisy na opakowaniu: producent, EAN, SKU. Model zmyśla adresy i przestawia cyfry w kodach,
4. margines liczbowo i brak przycięcia,
5. rogi: brak plakietki, znaku i resztek po malowaniu,
6. bramka tła.

Z pierwszej rundy zwykle około 40 % kadrów jest bez wad. To normalne: generuj z zapasem i wymień
odstępstwa w raporcie, zamiast liczyć, że nikt nie zauważy.

## 7. Poprawianie wybranego kadru

Wybrany kadr podaj jako pierwszą referencję ("układ jak na PIERWSZEJ") i zmieniaj jedną rzecz na rundę.
Dobry układ zlecaj kilka razy: kadry w wyższej rozdzielczości rzadziej przekręcają drobny druk.

## 8. Wgranie na ofertę

Tylko na wyraźną prośbę. Galeria Allegro ma limit 16 zdjęć. Przed zmianą zapisz obecną listę zdjęć
oferty, żeby dało się wrócić do poprzedniej kolejności.
