import json

# Otwórz plik phones.data.json
with open('../web_scraping/phones_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# stwórz funkcję, która usunie jednostki dla parametrów z wartościami liczbowymi np.'100 GB' -> '100'
def remove_units(data, params):
    for phone in data:
        for param in params:
            # uwzględnij sytuację, gdy nie istnieje taki parametr dla tego telefonu
            try:
                # usuń wszystkie znaki nie będące cyframi
                phone[param] = float(''.join([char for char in phone[param] if char.isdigit() or char == '.']))
            except:
                phone[param] = None
    return data


# stwórz funkcję, która usunie telefony, które nie mają w ogóle podanego parametru
def remove_phones_without_param(data, param):
    data = [phone for phone in data if param in phone]
    return data

def remove_comma_from_price(price):
    return price.replace(',', '')