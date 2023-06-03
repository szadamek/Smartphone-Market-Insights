import pandas as pd
import matplotlib.pyplot as plt
import json

# Dane telefonów
# Pobierz dane telefonów z pliku phones_data.json, ale interesuje nas tylko marka, jakość aparatu i pamięć wbudowana
with open('../web_scraping/phones_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Gdy telefon nie ma parametru "Rozdzielczość aparatu tylnego", "Wbudowana pamięć" lub "Marka telefonu", ustaw wartość na None
# Weź pod uwagę tylko te telefony, które mają wszystkie te parametry
data = [phone_data for phone_data in data if 'Rozdzielczość aparatu tylnego' in phone_data and 'Wbudowana pamięć' in phone_data and 'Marka telefonu' in phone_data]

# Weź tylko markę, jakość aparatu i pamięć wbudowaną
data = [{'Marka telefonu': phone_data['Marka telefonu'],
         'Rozdzielczość aparatu tylnego': phone_data['Rozdzielczość aparatu tylnego'],
         'Wbudowana pamięć': phone_data['Wbudowana pamięć']}
        for phone_data in data]

# Z jakości aparatu weź tylko liczbę bez napisu Mpx, a z pamięci wbudowanej weź tylko liczbę bez napisu GB
for phone_data in data:
    phone_data['Rozdzielczość aparatu tylnego'] = float(phone_data['Rozdzielczość aparatu tylnego'].split(' ')[0])
    if phone_data['Wbudowana pamięć'] in ['inna', 'brak pamięci']:
        phone_data['Wbudowana pamięć'] = None
    else:
        try:
            phone_data['Wbudowana pamięć'] = float(phone_data['Wbudowana pamięć'].split(' ')[0])
        except ValueError:
            phone_data['Wbudowana pamięć'] = None

# Tworzenie ramki danych z danymi telefonów
df = pd.DataFrame(data)

# Wykres punktowy
plt.figure(figsize=(10, 6))
plt.scatter(df["Rozdzielczość aparatu tylnego"], df["Wbudowana pamięć"], c='b', alpha=0.5)

# Dodawanie etykiet dla każdego punktu
for i in range(len(df)):
    plt.annotate(df["Marka telefonu"][i], (df["Rozdzielczość aparatu tylnego"][i], df["Wbudowana pamięć"][i]),
                 fontsize=8, ha='center', va='center')

# Ustawianie tytułów i etykiet osi
plt.title("Zależność pomiędzy jakością aparatu a ilością pamięci wbudowanej", fontsize=12, fontweight='bold')
plt.xlabel("Rozdzielczość aparatu tylnego", fontsize=10)
plt.ylabel("Wbudowana pamięć", fontsize=10)

# Ustawianie siatki
plt.grid(True, linestyle='--', alpha=0.7)

# Wyświetlanie wykresu
plt.tight_layout()
plt.show()
