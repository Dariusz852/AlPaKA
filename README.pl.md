# <code style="color : Blue">AlPaKA</code>

Pythonowa aplikacja do pobierania wiadomości z serwisu [Onet.pl](https://www.onet.pl/). 

![screenshot](./Tekstury/Lama_mod_3.png)

## <code style="color : Blue">Wprowadzenie</code>

Aplikacja napisana w pythonie pozwalająca pobrać wiadomości zamieszczone w serwisie [Onet.pl](https://www.onet.pl/). Pozyskiwanie danych odbywa się za pomocą metody webscrapingu. Dane są pozyskiwane według zadanych przez użytkownika dat początku i końca. Kod wykorzystje pythonowe biblioteki, takie jak:
* [os](https://docs.python.org/3/library/os.html)
* [pathlib](https://docs.python.org/3/library/pathlib.html)
* [tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
* [PIL](https://pillow.readthedocs.io/en/stable/)
* [pyglet](https://pypi.org/project/pyglet/)
* [datetime](https://docs.python.org/3/library/datetime.html)
* [re](https://docs.python.org/3/library/re.html)
* [requests](https://pypi.org/project/requests/)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
* [pandas](https://pandas.pydata.org/)
* [time](https://docs.python.org/3/library/time.html)
* [threading](https://docs.python.org/3/library/threading.html)

Biblioteki te są niezbędne do uruchomiania aplikacji. 

## <code style="color : Blue">Uruchamianie</code>
Aby uruchomić aplikacje należy umieścić pliki z repozytorium na pulpicie użytkownika. Akcja ta jest niezbędna, ze względu na to, że AlPaKA w pierwszej kolejności ustawia ścieżkę dostępu do pulipitu użytkownika (w oparciu o domyślną ścieżkę "home" na komputerze użytkownika). 

Uruchomienie aplikacji wywołuje interfejs użytkownika, a użytkownik zostaje poproszony o podjęcie interakcji.

### <code style="color : Blue">Język</code>
Użytkownik zostaje zapytany o wybór języka: polski lub angielski.

### <code style="color : Blue">Data początku i data końca</code>
Użytkownik zostaje zapytany o to z jakich dat chce pozyskać wiadomości z serwisu [Onet.pl](https://www.onet.pl/). Użytkownik musi podać dwie daty - początku i końca przeszukiwanego zakresu. Ważne, aby podane daty były z zakresu od 2010-01-01 do daty dnia dzisiejszej. Podane daty od użytkownika muszą być różne lub takie same.

## <code style="color : Blue">Działanie</code>
Wprowadzone przez użytkownika informacje są wykorzystywane przez AlPaKĘ do pozyskiwania wiadomości ze stron [archiwum](https://wiadomosci.onet.pl/archiwum/) z serwisu [Onet.pl](https://www.onet.pl/). Dane są zbierane w formacie tabeli o następujących kolumnach:
* Nagłówek
* Lead wiadomości
* Treść wiadomości
* Data umieszczenia wiadomości
* Autor tekstu
* Link do wiadomości 

Pozyskane dane są na koniec działania programu zapisywane w pliku `Data_AlPaKA.csv` na pulpicie użytkownika.

## <code style="color : Blue">Uwagi</code>
AlPaKA jest aplikacją hobbistyczną napisaną przez użytkownika githube'a [`Dariusz852`](https://github.com/Dariusz852). 

Dane pozyskane w ramach aplikacji są informacjami ogólnodostępnymi z serwisu [Onet.pl](https://www.onet.pl/).

Wizerunek Lamy użyty w aplikacji i w dokumentacji został wykorzystany za jej zgodą. Rozprzestrzenianie go poza te dwa obszary jest zabronione. 

Wykorzystane w aplikacji obrazy flag pochodzą z odpowiednich stron z serwisu [Wikipedia](https://pl.wikipedia.org/).

Plansze wzorowane na anime Neon Genesis Evangelion z roku 1995 pochodzą z generatora plansz [evangelion](https://evangelion.boodoo.co/).

W aplikacji wykorzystywana jest czcionka [OpenDyslexic](https://opendyslexic.org/).
