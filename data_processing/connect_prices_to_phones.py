import json


# Wczytaj dane z pliku JSON
with open('../web_scraping/phones_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('../web_scraping/phones_data_new.json', 'r', encoding='utf-8') as file:
    data2 = json.load(file)

# dodaj do data cechę 'Cena' z data2 dopasowując po 'url'
for phone in data:
    for phone2 in data2:
        if phone['url'] == phone2['url']:
            phone['Cena'] = phone2['Cena']
            break

# zapisz do pliku
with open('../web_scraping/phones_data_connected.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)