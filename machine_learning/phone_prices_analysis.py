import json
import matplotlib.pyplot as plt
from data_processing.data_processing_file import remove_units
import statistics

# Wczytaj dane z pliku JSON
with open('../web_scraping/phones_data_connected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# usuń telefony, które nie mają w ogóle parametru marka telefonu, model telefonu, cena, rozdzielczość aparatu tylnego, pojemność baterii
data = [phone for phone in data if 'Marka telefonu' in phone]
data = [phone for phone in data if 'Model telefonu' in phone]
data = [phone for phone in data if 'Cena' in phone]
data = [phone for phone in data if 'Rozdzielczość aparatu tylnego' in phone]
data = [phone for phone in data if 'Pojemność akumulatora' in phone]

# usuń jednostki z parametrów, które są liczbami
data = remove_units(data, ['Cena', 'Rozdzielczość aparatu tylnego', 'Pojemność akumulatora'])

# Przygotuj listy na cechy i ceny telefonów
marki = []
modele = []
ceny = []

# Przetwórz dane i wyodrębnij interesujące cechy oraz ceny
for telefon in data:
    marka = telefon['Marka telefonu']
    model = telefon['Model telefonu']
    cena = telefon['Cena']

    # Dodaj cechy i ceny do odpowiednich list
    marki.append(marka)
    modele.append(model)
    ceny.append(cena)

# Wykonaj analizę cen telefonów
srednia_cena = statistics.mean(ceny)
mediana_cen = statistics.median(ceny)
minimalna_cena = min(ceny)
maksymalna_cena = max(ceny)

# Wyświetl wyniki analizy
print('Statystyki cen telefonów:')
print('Średnia cena:', srednia_cena)
print('Mediana cen:', mediana_cen)
print('Minimalna cena:', minimalna_cena)
print('Maksymalna cena:', maksymalna_cena)

# Wygeneruj wykres histogramu cen
plt.hist(ceny, bins=10, edgecolor='black')
plt.xlabel('Cena')
plt.ylabel('Liczba telefonów')
plt.title('Rozkład cen telefonów')
plt.show()

# Przygotuj listy na cechy i ceny telefonów
marki = []
modele = []
ceny = []
rozdzielczosci = []
baterie = []

# Przetwórz dane i wyodrębnij interesujące cechy oraz ceny
for telefon in data:
    marka = telefon['Marka telefonu']
    model = telefon['Model telefonu']
    cena = telefon['Cena']
    rozdzielczosc = telefon['Rozdzielczość aparatu tylnego']
    pojemnosc_baterii = telefon['Pojemność akumulatora']

    # Dodaj cechy i ceny do odpowiednich list
    marki.append(marka)
    modele.append(model)
    ceny.append(cena)
    rozdzielczosci.append(rozdzielczosc)
    baterie.append(pojemnosc_baterii)

# Wykres zależności rozdzielczości aparatu tylnego od ceny
plt.scatter(ceny, rozdzielczosci)
plt.xlabel('Cena')
plt.ylabel('Rozdzielczość aparatu tylnego')
plt.title('Zależność cen telefonów od rozdzielczości aparatu')
plt.show()

# Wykres zależności pojemności baterii od ceny
plt.scatter(ceny, baterie)
plt.xlabel('Cena')
plt.ylabel('Pojemność baterii')
plt.title('Zależność cen telefonów od pojemności baterii')
plt.show()

# Wykres słupkowy przedstawiający liczbę telefonów dla każdej marki
unikalne_marki = list(set(marki))
liczba_telefonow_marki = [marki.count(marka) for marka in unikalne_marki]

plt.bar(unikalne_marki, liczba_telefonow_marki)
plt.xlabel('Marka telefonu')
plt.ylabel('Liczba telefonów')
plt.title('Liczba telefonów dla każdej marki')
plt.xticks(rotation='vertical')
plt.show()
