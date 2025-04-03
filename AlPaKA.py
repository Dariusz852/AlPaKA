# -*- coding: utf-8 -*-

################## Pakiety
import os
from pathlib import Path
from tkinter import Tk, Label, Button, Frame, StringVar, Entry, ttk
from PIL import ImageTk, Image
import pyglet
import datetime
import re
import requests
from bs4 import BeautifulSoup
import pandas
import time
import threading

################## Definicje funkcji
# Zmiana ścieżki
def sciezka_zmien(gdzie_idziemy):
    
    # Warunek na zmiane ścieżki roboczej - "pulpit", "tekstury" i "czcionka"
    if gdzie_idziemy == 'pulpit':
        os.chdir('..')
    elif gdzie_idziemy == 'czcionka':
        os.chdir(str(os.getcwd()+'\\Czcionka'))
    elif gdzie_idziemy == 'tekstury':
        os.chdir(str(os.getcwd()+'\\Tekstury'))

# Zmiana scen
def zmiana_scena(stara_scena, nowa_scena):
    
    # Zapomnienie starej scenie i wyświetlenie nowej sceny
    stara_scena.forget()
    nowa_scena.pack(fill="both", expand=True)
    
# Funkcja do sprawdzania poprawności pierwszej daty
def czy_data_pierwsza_ok(data):
    
    # Sprawdzenie czy można zamienić otrzymaną "datę" na datę oraz sprawdzenie czy rok daty jest >= 2010
    try:
        data = datetime.datetime.strptime(data.get(), "%Y-%m-%d").date()
    except ValueError:
        zmiana_scena(Scena_data_raz, Scena_blad_data)
    else:
        if data.year >= 2010:    
            zmiana_scena(Scena_data_raz, Scena_data_dwa)
        else:
            zmiana_scena(Scena_data_raz, Scena_blad_data)
            
# Funkcja do sprawdzania poprawności drugiej daty
def czy_data_druga_ok(data1, data2):
    
    # Sprawdzenie czy można zamienić otrzymaną "datę" na datę oraz sprawdzenie czy rok daty jest >= 2010, a także porównanie obu dat
    try:
        data_2 = datetime.datetime.strptime(data2.get(), "%Y-%m-%d").date()
        data_1 = datetime.datetime.strptime(data1.get(), "%Y-%m-%d").date()
    except ValueError:
        zmiana_scena(Scena_data_dwa, Scena_blad_data)
    else:
        if data_2.year >= 2010 and data_1 <= data_2: 
            
            # Przypisanie zakresu dat do sceny i przejście dalej
            napis_fin_2 = Label(Scena_data_fin, text=data1.get(), font=('OpenDyslexic-Regular',15), fg="blue")
            napis_fin_2.pack(padx=50, pady=40)
            napis_fin_3 = Label(Scena_data_fin, text=data2.get(), font=('OpenDyslexic-Regular',15), fg="blue")
            napis_fin_3.pack(padx=50, pady=60)
            zmiana_scena(Scena_data_dwa, Scena_data_fin)
            
        else:
            zmiana_scena(Scena_data_dwa, Scena_blad_data)
            
# Poprawienie daty, gdy użytkownik wprowadził miesiąc lub dzień bez zera
def Czy_daty_mają_dobry_format(Listaaa):
    
    # Poprawa 
    if len(Listaaa[1]) != 2:
        Listaaa[1] = '0' + Listaaa[1]
    if len(Listaaa[2]) != 2:
        Listaaa[2] = '0' + Listaaa[2]            
    return Listaaa
            
# Funkcja do webscrapingu
def webscraping_onet(stara_scena, nowa_scena, data1, data2):
    
    # Deklaracja tablicy do zbierania danych
    global tabela_dane_fin
    tabela_dane_fin = pandas.DataFrame()
    
    # Zmiana sceny z dat_fin na webscraping
    zmiana_scena(stara_scena, nowa_scena)
    
    # Ile czasu mineło pomiędzy datami
    data_2 = datetime.datetime.strptime(data2.get(), "%Y-%m-%d").date()
    data_1 = datetime.datetime.strptime(data1.get(), "%Y-%m-%d").date()
    ile_dni = re.split(" ",str(data_2 - data_1))
    ile_dni = ile_dni[0]
    
    # przerobienie daty
    data1 = re.split("-", data1.get())
    data2 = re.split("-", data2.get())
    
    # Poprawienie dat
    data1 = Czy_daty_mają_dobry_format(data1)
    data2 = Czy_daty_mają_dobry_format(data2)
    
    # Poczekanie dwóch sekund
    #time.sleep(2)
    
    # Sprawdzenie czy ile_dni jest zerem, jeśali tak to pętla wykona się tylko raz
    if ile_dni.find(":") == 1:
        
        # Link do strony onetu i parsowanie
        onet_link = requests.get('https://wiadomosci.onet.pl/archiwum/'+data1[0]+"-"+data1[1]+"-"+data1[2])
        onet_link = BeautifulSoup(onet_link.content, 'html.parser')
        
        # Wyodrębnienie listy linków do pozyskiwania danych
        onet_linki_przeglad=onet_link.find_all('a', class_='itemTitle')
        
        # Dodanie paska
        pasek_web = ttk.Progressbar(nowa_scena, orient="horizontal", length=150, maximum=len(onet_linki_przeglad))
        pasek_web['value'] = 0
        pasek_web.pack(pady=20)
        
        # Dodanie Lamy
        plansza_web = Image.open("Lama_mod_3.png")
        plansza_web = ImageTk.PhotoImage(plansza_web)
        pla_web = Label(nowa_scena, image = plansza_web )
        pla_web.pack()
        
        # Pozyskiwanie danych - autor, nagłówek, Lead i treść artykułów, data, link
        for i in range(0,len(onet_linki_przeglad),1):
            
            # Odczytywanie linku i wczytywanie linku z listy
            onet_link = requests.get(onet_linki_przeglad[i].get('href'))
            onet_link = BeautifulSoup(onet_link.content, 'html.parser')
            
            # Ustawienie w metodzie try, bo może się zdarzyć, że źle wczyta się strona
            try: 
                
                # Nagłówek
                tabela_dane_fin.loc[i,'Nagłówek'] = onet_link.find('h1', class_='mainTitle').get_text().replace("  ", "").replace("\n", "")

                # Lead artykułów 
                tabela_dane_fin.loc[i,'Lead'] = onet_link.find_all('div', class_='lead')[0].get_text()

                # Treść artykułów 
                tabela_dane_fin.loc[i,'Treść'] = onet_link.find_all('div', class_='detail intext articleBody')[0].get_text().replace("  ", "").replace("\n", "")

                # Data artykułów 
                tabela_dane_fin.loc[i,'Data'] = onet_link.find_all('time', class_='datePublished')[0].get_text().replace("  ", "").replace("\n", "")

                # Autor 
                tabela_dane_fin.loc[i,'Autor'] = onet_link.find_all('span', class_='name')[0].get_text()

                # Zapisywanie linku do tabeli finalnej
                tabela_dane_fin.loc[i,'Link'] = onet_linki_przeglad[i].get('href')
            
            except IndexError:
                
                # Zapisywanie linku do tabeli finalnej
                tabela_dane_fin.loc[i,'Link'] = onet_linki_przeglad[i].get('href')
                
            # Komunikat o postępie
            #print("Mam ", i)
            pasek_web['value'] += 1
            nowa_scena.update()
            time.sleep(1)
                            
    else:
        
        # lista na linki
        lista_web_onet = []
        
        # Pętla dla różnych dat
        for k in range(0,int(ile_dni)+1,1):
            
            # Konstrukcja daty do szukania
            data_szukana = str(data_2 + datetime.timedelta(days=k ) )
            
            # Link do strony onetu i parsowanie
            onet_link = requests.get('https://wiadomosci.onet.pl/archiwum/'+data_szukana)
            onet_link = BeautifulSoup(onet_link.content, 'html.parser')
            
            # Wyodrębnienie listy linków do pozyskiwania danych
            onet_linki_przeglad=onet_link.find_all('a', class_='itemTitle')
        
            # Pętla do zbierania listy na linki
            for krokkk in range(0,len(onet_linki_przeglad),1):
                
                # Uzupełnienie listy
                lista_web_onet.append(onet_linki_przeglad[krokkk])
                
        # Dodanie paska
        pasek_web = ttk.Progressbar(nowa_scena, orient="horizontal", length=150, maximum=len(lista_web_onet))
        pasek_web['value'] = 0
        pasek_web.pack(pady=20)
        
        # Dodanie Lamy
        plansza_web = Image.open("Lama_mod_3.png")
        plansza_web = ImageTk.PhotoImage(plansza_web)
        pla_web = Label(nowa_scena, image = plansza_web )
        pla_web.pack()
                
        # Pozyskiwanie danych - autor, nagłówek, Lead i treść artykułów, data, link
        for i in range(0,len(lista_web_onet),1):
            
            # Odczytywanie linku i wczytywanie linku z listy
            onet_link = requests.get(lista_web_onet[i].get('href'))
            onet_link = BeautifulSoup(onet_link.content, 'html.parser')
            
            # Ustawienie w metodzie try, bo może się zdarzyć, że źle wczyta się strona
            try: 
                
                # Nagłówek
                tabela_dane_fin.loc[i,'Nagłówek'] = onet_link.find('h1', class_='mainTitle').get_text().replace("  ", "").replace("\n", "")

                # Lead artykułów 
                tabela_dane_fin.loc[i,'Lead'] = onet_link.find_all('div', class_='lead')[0].get_text()

                # Treść artykułów 
                tabela_dane_fin.loc[i,'Treść'] = onet_link.find_all('div', class_='detail intext articleBody')[0].get_text().replace("  ", "").replace("\n", "")

                # Data artykułów 
                tabela_dane_fin.loc[i,'Data'] = onet_link.find_all('time', class_='datePublished')[0].get_text().replace("  ", "").replace("\n", "")

                # Autor 
                tabela_dane_fin.loc[i,'Autor'] = onet_link.find_all('span', class_='name')[0].get_text()

                # Zapisywanie linku do tabeli finalnej
                tabela_dane_fin.loc[i,'Link'] = lista_web_onet[i].get('href')
            
            except IndexError:
                
                # Zapisywanie linku do tabeli finalnej
                tabela_dane_fin.loc[i,'Link'] = lista_web_onet[i].get('href') 
                
            # Komunikat o postępie
            #print("Mam ", i)
            pasek_web['value'] += 1
            nowa_scena.update()
            time.sleep(1)
        
    # Zmiana ścieżki
    sciezka_zmien("pulpit")
    
    # Eksport tabeli finalnej
    tabela_dane_fin.to_csv("Data_AlPaKA.csv",index = False, sep=',', encoding='utf-8-sig')
    
    # Zmiana sceny
    zmiana_scena(nowa_scena, Scena_koniec)
    
# Funkcja zamykająca program
def koniec():
    
    # Zamknięcie pracy programu
    Scena_koniec.destroy()
    root.destroy()
  
# Zmiana scen i wybór wartości napisów dla języka w aplikacji 
def wybór_jezyk_i_scena(stara_scena, nowa_scena, jaki_jezyk):
    
    # Zmiana sceny
    zmiana_scena(stara_scena, nowa_scena)
    
    # Ustawienie globalnej zmiennej dla dat
    global data_jeden
    global data_dwa    

    # Wybór napisów dla aplikacji - jezyk polski lub jezyk angielski
    if jaki_jezyk=="PL":
        
        ######### Ustawienia polskie dla planszy z obaśnieniami
        # Napisy informujące o sposobie działania programu wraz z guzikiem "Dalej"
        opis_1 = Label(Scena_opis, text="Program służy do pobierania wiadomości", font=('OpenDyslexic-Regular',30), fg="blue")
        opis_1.pack(padx=50, pady=20)
        opis_2 = Label(Scena_opis, text="z serwisu Onet na określone daty", font=('OpenDyslexic-Regular',30), fg="blue")
        opis_2.pack(padx=50, pady=120)
        opis_guzik = Button(Scena_opis, text = "Dalej",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: zmiana_scena(Scena_opis,Scena_NGE))
        opis_guzik.place(x=550, y=450)
        
        ######### Ustawienia polskie dla planszy z NGE
        # Przygotowanie planszy NGE dla języka pl i wgranie jej na scenę
        plansza_NGE = Image.open("16-9 PL.png")
        plansza_NGE = ImageTk.PhotoImage(plansza_NGE, master=Scena_NGE)
        pla_NGE = Label(Scena_NGE, image = plansza_NGE )
        pla_NGE.image = plansza_NGE
        pla_NGE.grid(row=0, column=0)
          
        # Guzik "Dalej" do przejścia dalej
        guzik_dalej = Button(Scena_NGE, text = "Dalej",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: zmiana_scena(Scena_NGE,Scena_data_raz))
        guzik_dalej.place(x=900, y=500)
        
        ######### Ustawienia polskie dla planszy z pierwszą datą
        # Plansza z napisem "Podaj date początku" i formatu daty
        data_napis_1 = Label(Scena_data_raz, text="Podaj date początku.", font=('OpenDyslexic-Regular',25), fg="blue")
        data_napis_1.pack(padx=50, pady=20)
        data_napis_2 = Label(Scena_data_raz, text="Date podaj w formacie: YYYY-MM-DD.", font=('OpenDyslexic-Regular',25), fg="blue")
        data_napis_2.pack(padx=50, pady=120)
        
        # Przygotowanie zmiennej data dla planszy z pierwszą datą
        data_jeden = StringVar(value="YYYY-MM-DD")
        data = Entry(Scena_data_raz, textvariable=data_jeden)
        data.pack()
        
        # Przygotowanie guzika "Dalej" po wpisaniu pierwszej daty
        opis_guzik = Button(Scena_data_raz, text = "Dalej",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: czy_data_pierwsza_ok(data_jeden))
        opis_guzik.place(x=550, y=450)
        
        ######### Ustawienia polskie dla planszy z błędem daty
        # Napisy informujące o błędzie wraz z guzikiem "Dalej"
        blad_1 = Label(Scena_blad_data, text="Data musi być w formacie: YYYY-MM-DD.", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_1.pack(padx=50, pady=20)
        blad_2 = Label(Scena_blad_data, text="Rok daty musi być większy", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_2.pack(padx=50, pady=40)              
        blad_3 = Label(Scena_blad_data, text="bądź równy wartości '2010'.", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_3.pack(padx=50, pady=50)                
        blad_4 = Label(Scena_blad_data, text="Druga data musi być wcześniejsza bądź równa dacie pierwszej.", font=('OpenDyslexic-Regular',15), fg="blue")
        blad_4.pack(padx=50, pady=70)
        opis_guzik = Button(Scena_blad_data, text = "Dalej",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: zmiana_scena(Scena_blad_data,Scena_data_raz))
        opis_guzik.place(x=550, y=550)
        
        ######### Ustawienia polskie dla planszy z drugą datą
        # Plansza z napisem "Podaj date końca" i formatu daty
        data_napisy_1 = Label(Scena_data_dwa, text="Podaj date końca.", font=('OpenDyslexic-Regular',25), fg="blue")
        data_napisy_1.pack(padx=50, pady=20)
        data_napisy_2 = Label(Scena_data_dwa, text="Date podaj w formacie: YYYY-MM-DD.", font=('OpenDyslexic-Regular',25), fg="blue")
        data_napisy_2.pack(padx=50, pady=120)
        
        # Przygotowanie zmiennej data dla planszy z drugą datą
        data_dwa = StringVar(value="YYYY-MM-DD")
        data2 = Entry(Scena_data_dwa, textvariable=data_dwa)
        data2.pack()
        
        # Przygotowanie guzika "Dalej" po wpisaniu drugiej daty
        opis_guzik2 = Button(Scena_data_dwa, text = "Dalej",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: czy_data_druga_ok(data_jeden,data_dwa))
        opis_guzik2.place(x=550, y=450)
        
        ######### Ustawienia polskie dla planszy z datą - wersja finalna
        # Napisy informacyjne o tym jakie wartości się wybrało
        napis_fin_1 = Label(Scena_data_fin, text="Wybrałeś zakres:", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_fin_1.pack(padx=50, pady=20)
        
        # Przyciski        
        opis_napis_fin = Button(Scena_data_fin, text = "Dalej",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: webscraping_onet(Scena_data_fin,Scena_onet,data_jeden,data_dwa))
        opis_napis_fin.place(x=550, y=450)
        
        ######### Ustawienia polskie dla planszy z webscrapingiem
        # Napis o informacji
        napis_web_1 = Label(Scena_onet, text="Progres", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_web_1.pack(padx=50, pady=20)
        
        ######### Ustawienia polskie dla planszy z końcem pracy programu
        # Napis o informacji
        napis_the_end_1 = Label(Scena_koniec, text="Koniec", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_the_end_1.pack(pady=20)
        napis_the_end_2 = Label(Scena_koniec, text="Dzięki za użycie programu :)", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_the_end_2.pack(pady=40)
        
        # Przygotowanie guzika "Zamknij" po wpisaniu drugiej daty
        guzik_the_end = Button(Scena_koniec, text = "Zamknij",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: koniec())
        guzik_the_end.place(x=550, y=450)
    
    elif jaki_jezyk=="ENG":
        
        ######### Ustawienia angielskie dla planszy z obaśnieniami
        # Napisy informujące o sposobie działania programu wraz z guzikiem "Next"
        opis_1 = Label(Scena_opis, text="The program is used for receiving news", font=('OpenDyslexic-Regular',27), fg="blue")
        opis_1.pack(padx=50, pady=20)
        opis_2 = Label(Scena_opis, text="from the Onet service on specific dates", font=('OpenDyslexic-Regular',27), fg="blue")
        opis_2.pack(padx=50, pady=120)
        opis_guzik = Button(Scena_opis, text = "Next",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: zmiana_scena(Scena_opis,Scena_NGE))
        opis_guzik.place(x=550, y=450)
        
        ######### Ustawienia angielskie dla planszy z NGE 
        # Przygotowanie planszy NGE dla języka eng i wgranie jej na scenę
        plansza_NGE = Image.open("16-9 ENG.png")
        plansza_NGE = ImageTk.PhotoImage(plansza_NGE, master=Scena_NGE)
        pla_NGE = Label(Scena_NGE, image = plansza_NGE )
        pla_NGE.image = plansza_NGE
        pla_NGE.grid(row=0, column=0)

        # Guzik "ok" do przejścia dalej
        guzik_ok = Button(Scena_NGE, text = "Next",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: zmiana_scena(Scena_NGE,Scena_data_raz))
        guzik_ok.place(x=900, y=500)

        ######### Ustawienia angielskie dla planszy z pierwszą datą
        # Plansza z napisem "Podaj date początku" i formatu daty
        data_napis_1 = Label(Scena_data_raz, text="Provide the start date.", font=('OpenDyslexic-Regular',20), fg="blue")
        data_napis_1.pack(padx=50, pady=20)
        data_napis_2 = Label(Scena_data_raz, text="The date in the format: YYYY-MM-DD.", font=('OpenDyslexic-Regular',20), fg="blue")
        data_napis_2.pack(padx=50, pady=120)
        
        # Przygotowanie zmiennej data dla planszy z pierwszą datą
        data_jeden = StringVar(value="YYYY-MM-DD")
        data = Entry(Scena_data_raz, textvariable=data_jeden)
        data.pack()
        
        # Przygotowanie guzika "Next" po wpisaniu pierwszej daty
        opis_guzik = Button(Scena_data_raz, text = "Next",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: czy_data_pierwsza_ok(data_jeden))
        opis_guzik.place(x=550, y=450)
        
        ######### Ustawienia angielskie dla planszy z błędem daty
        # Napisy informujące o błędzie wraz z guzikiem "Next"
        blad_1 = Label(Scena_blad_data, text="The date must be in the format: YYYY-MM-DD.", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_1.pack(padx=50, pady=20)
        blad_2 = Label(Scena_blad_data, text="The year of the date must be", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_2.pack(padx=50, pady=40)              
        blad_3 = Label(Scena_blad_data, text="greater than or equal to '2010'.", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_3.pack(padx=50, pady=50)                
        blad_4 = Label(Scena_blad_data, text="The second date must be earlier than", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_4.pack(padx=50, pady=55)
        blad_5 = Label(Scena_blad_data, text="or equal to the first date.", font=('OpenDyslexic-Regular',20), fg="blue")
        blad_5.pack(padx=50, pady=60)
        opis_guzik = Button(Scena_blad_data, text = "Next",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: zmiana_scena(Scena_blad_data,Scena_data_raz))
        opis_guzik.place(x=1000, y=550)

        ######### Ustawienia angielskie dla planszy z drugą datą
        # Plansza z napisem "Podaj date końca" i formatu daty
        data_napisy_1 = Label(Scena_data_dwa, text="Provide the end date.", font=('OpenDyslexic-Regular',25), fg="blue")
        data_napisy_1.pack(padx=50, pady=20)
        data_napisy_2 = Label(Scena_data_dwa, text="The date in the format: YYYY-MM-DD.", font=('OpenDyslexic-Regular',25), fg="blue")
        data_napisy_2.pack(padx=50, pady=120)
        
        # Przygotowanie zmiennej data dla planszy z drugą datą
        data_dwa = StringVar(value="YYYY-MM-DD")
        data2 = Entry(Scena_data_dwa, textvariable=data_dwa)
        data2.pack()
        
        # Przygotowanie guzika "Next" po wpisaniu drugiej daty
        opis_guzik2 = Button(Scena_data_dwa, text = "Next",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: czy_data_druga_ok(data_jeden,data_dwa))
        opis_guzik2.place(x=550, y=450)
        
        ######### Ustawienia angielskiego dla planszy z datą - wersja finalna
        # Napisy informacyjne o tym jakie wartości się wybrało
        napis_fin_1 = Label(Scena_data_fin, text="You have chosen the range:", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_fin_1.pack(padx=50, pady=20)
        
        # Przyciski        
        opis_napis_fin = Button(Scena_data_fin, text = "Next",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: webscraping_onet(Scena_data_fin,Scena_onet,data_jeden,data_dwa))
        opis_napis_fin.place(x=550, y=450)
        
        ######### Ustawienia angielskiego dla planszy z webscrapingiem
        # Napis o informacji
        napis_web_1 = Label(Scena_onet, text="Progress", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_web_1.pack(padx=50, pady=20)
        
        ######### Ustawienia angielskiego dla planszy z końcem pracy programu
        # Napis o informacji
        napis_the_end_1 = Label(Scena_koniec, text="The End", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_the_end_1.pack(pady=20)
        napis_the_end_2 = Label(Scena_koniec, text="Thank you for using this program :)", font=('OpenDyslexic-Regular',15), fg="blue")
        napis_the_end_2.pack(pady=40)
        
        # Przygotowanie guzika "Zamknij" po wpisaniu drugiej daty
        guzik_the_end = Button(Scena_koniec, text = "Close",font=('OpenDyslexic-Regular',30), fg="blue", command=lambda: koniec())
        guzik_the_end.place(x=550, y=350)

################## Main
# Ścieżka do plików
os.chdir(str(Path.home())+'\\Desktop')

# Zmiana ścieżki do czcionki
sciezka_zmien("czcionka")  

# Wczytanie czcionki
pyglet.font.add_file('OpenDyslexic-Regular.otf')

# Przejście do folderu z teksturami
sciezka_zmien("pulpit") 
sciezka_zmien("tekstury") 

# Przygotowanie rozmiaru i nazwy okna aplikacji
root = Tk()
root.title("AlPaKA")
root.geometry("1280x720")

################## Scena startowa
Start = Frame(root)

# Lokalizacja i nazwa tekstu z nazwą programu
AlPaKA = Label(Start, text="AlPaKA", font=('OpenDyslexic-Regular',150), fg="blue")
AlPaKA.pack(padx=50, pady=100)

# Wczytanie obrazków flag i modyfikacja rozmiaru
flaga_polska = Image.open("Flaga_PL_mod.png")
flaga_polska = flaga_polska.resize((300, 150))
flaga_polska = ImageTk.PhotoImage(flaga_polska, master=Start)
flaga_anglia = Image.open("Flaga_ENG.png")
flaga_anglia = flaga_anglia.resize((300, 150))
flaga_anglia = ImageTk.PhotoImage(flaga_anglia, master=Start)

# Guzik Polska
polska_guzik = Button(Start,command=lambda: wybór_jezyk_i_scena(Start,Scena_opis,"PL"), image = flaga_polska )
polska_guzik.place(x=314, y=450)

# Guzik Anglia
anglia_guzik = Button(Start, command=lambda: wybór_jezyk_i_scena(Start,Scena_opis, "ENG"), image = flaga_anglia )
anglia_guzik.place(x=814, y=450)  

################## Scena z opisem aplikacji
Scena_opis = Frame(root)

# Reszta elementów strony jest zakodowana w funkcji wybór_jezyk_i_scena

################## Scena z planszą NGE
Scena_NGE = Frame(root)

# Reszta elementów strony jest zakodowana w funkcji wybór_jezyk_i_scena

################## Scena z datą pierwszą
Scena_data_raz = Frame(root)

### Poniższa plansza jest zakodowany w funkcji wybór_jezyk_i_scena  

################## Scena z datą drugą
Scena_data_dwa = Frame(root)

### Poniższa plansza jest zakodowany w funkcji wybór_jezyk_i_scena  

################## Scena z błedem daty
Scena_blad_data = Frame(root)

### Poniższa plansza jest zakodowany w funkcji wybór_jezyk_i_scena 

################## Scena z podsumowaniem dat
Scena_data_fin = Frame(root)

### Poniższa plansza jest zakodowany w funkcji wybór_jezyk_i_scena

################## Scena z pobieraniem wiadomości
Scena_data_fin = Frame(root)

### Poniższa plansza jest zakodowany w funkcji wybór_jezyk_i_scena

################## Scena z podsumowaniem i końcem
Scena_data_fin = Frame(root)

### Poniższa plansza jest zakodowany w funkcji wybór_jezyk_i_scena

################## Scena z webscrapingiem Onetu
Scena_onet = Frame(root)

### Poniższa plansza jest zakodowany w funkcji wybór_jezyk_i_scena

################## Scena z końcem pracy programu
Scena_koniec = Frame(root)

### Poniższa plansza jest zakodowany w funkcjach: wybór_jezyk_i_scena i webscraping_onet

################## Przygotowanie threadinga
threading.Thread(target=webscraping_onet).start()

################## Uruchomianie całego UI
# Wywołanie strony startowej na początek i uruchomienie całego UI
Start.pack(fill="both", expand=True)
root.mainloop()