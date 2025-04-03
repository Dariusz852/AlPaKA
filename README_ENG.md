# <code style="color : Blue">AlPaKA</code>

A Python application for fetching news from [Onet.pl](https://www.onet.pl/). 

![screenshot](./Tekstury/Lama_mod_3.png)

## <code style="color : Blue">Introduction</code>

An application written in Python that allows fetching news posted on [Onet.pl](https://www.onet.pl/). Data acquisition is performed using the web scraping method. The data is retrieved based on the start and end dates specified by the user. The code utilizes Python libraries such as:
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

These libraries are essential for running the application. 

## <code style="color : Blue">Execution</code>
To run the application, the files from the repository must be placed on the user's desktop. This action is necessary because AlPaKA first sets the access path to the user's desktop (based on the default "home" path on the user's computer).

Running the application launches the user interface, and the user is prompted to interact.

### <code style="color : Blue">Language</code>
The user is asked to choose a language: Polish or English.

### <code style="color : Blue">Start Date and End Date</code>
The user is asked to specify the dates from which they want to fetch news from  [Onet.pl](https://www.onet.pl/). The user must enter two dates – the start and end of the search range. It is important that the provided dates fall within the range from 2010-01-01 to the current date. The dates entered by the user can be different or the same.

## <code style="color : Blue">Operation</code>
The information provided by the user is used by AlPaKA to fetch news from the [archive](https://wiadomosci.onet.pl/archiwum/) pages of [Onet.pl](https://www.onet.pl/). The data is collected in a table format with the following columns:
* Nagłówek - Headline
* Lead - News Lead
* Treść - News Content
* Data - News Publication Date
* Autor - Author of the Text
* Link -  News Link

The retrieved data is saved at the end of the program's execution in a file named `Data_AlPaKA.csv` on the user's desktop.

## <code style="color : Blue">Notes</code>
AlPaKA is a hobby application written by the GitHub user [`Dariusz852`](https://github.com/Dariusz852). 

The data obtained through the application consists of publicly available information from [Onet.pl](https://www.onet.pl/).

The image of the Llama used in the application and documentation has been used with its consent. Redistribution outside these two areas is prohibited. 

The flags used in the application come from the respective pages on [Wikipedia](https://pl.wikipedia.org/).

The screens inspired by the 1995 anime Neon Genesis Evangelion come from the [evangelion](https://evangelion.boodoo.co/) screen generator.

The application uses the [OpenDyslexic](https://opendyslexic.org/) font.