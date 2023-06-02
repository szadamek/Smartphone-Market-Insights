import csv

input_file = '../web_scraping/dane.csv'

# Otwórz plik CSV do odczytu
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames  # Pobierz nagłówki z pliku CSV

    # Przeiteruj przez każdy wiersz pliku
    for row in reader:
        # Wyświetl wartości dla każdego nagłówka
        for header in headers:
            print(f"{header}: {row[header]}")
        print("--------------------")
