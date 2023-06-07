import json

# Otwórz plik JSON
with open('phones_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Otwórz plik 'phones.txt' w trybie do dopisywania
with open('phones.txt', 'a') as txt_file:
    # Iteruj przez elementy w pliku JSON
    for item in data:
        # Sprawdź, czy istnieje klucz 'url' dla danego elementu
        if 'url' in item:
            url = item['url']
            # Dopisz link do pliku 'phones.txt'
            txt_file.write(url + '\n')

print("Linki zostały wydobyte i zapisane w pliku 'phones.txt'")
