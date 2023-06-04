from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json

# Wczytanie danych z pliku
with open('../web_scraping/phones_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# z parametrów takich jak 'szerokość', 'wysokość', 'głębokość', 'waga', 'przekątna ekranu', 'rozdzielczość ekranu', 'częstotliwość procesora', 'pojemność akumulatora' wyciagnij liczbę
for phone in data:
    for param in ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']:
        # uwzględnij sytuację, gdy nie istnieje taki parametr dla tego telefonu
        try:
            # usuń wszystkie znaki nie będące cyframi
            phone[param] = float(''.join([char for char in phone[param] if char.isdigit() or char == '.']))
        except:
            phone[param] = None

# usuń telefony, które nie mają w ogóle parametru marka telefonu
data = [phone for phone in data if 'Marka telefonu' in phone]

# Przygotowanie danych treningowych
X = []
y = []
# weź tylko te telefony które mają wszystkie parametry kompletne włącznie z marką telefonu
for phone in data:
    if all([phone[param] is not None for param in
            ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']]):
        X.append([phone[param] for param in
                  ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']])
        y.append(phone['Marka telefonu'])

# Zakodowanie etykiet kategorii
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# normalizacja danych z bibliteki sklearn
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Inicjalizacja i trenowanie klasyfikatora k najbliższych sąsiadów
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Predykcja dla danych testowych
y_pred = knn.predict(X_test)

# Dekodowanie etykiet kategorii
y_pred = label_encoder.inverse_transform(y_pred)

# Wyświetlenie wyników predykcji
for i in range(len(X_test)):
    print('Dane wejściowe:', X_test[i])
    print('Oczekiwana marka telefonu:', label_encoder.inverse_transform([y_test[i]]))
    print('Przewidziana marka telefonu:', y_pred[i])
    print()

# Ocena dokładności modelu
accuracy = knn.score(X_test, y_test)
print('Dokładność modelu:', accuracy)
