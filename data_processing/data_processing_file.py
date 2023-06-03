import json

# Otwórz plik phones.data.json
with open('../web_scraping/phones_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Wyświetl parametry telefonów
for phone_data in data:
    print(phone_data)

# Możesz teraz wykorzystać odczytane parametry telefonów do dalszej obróbki
# np. przetwarzania, analizy itp.
