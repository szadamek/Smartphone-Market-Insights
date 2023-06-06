from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json
from skopt import BayesSearchCV
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

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
    if all([phone[param] is not None for param in ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']]):
        X.append([phone[param] for param in ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']])
        y.append(phone['Marka telefonu'])

# Zakodowanie etykiet kategorii
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definicja modelu KNN
knn = KNeighborsClassifier()

# Definicja przestrzeni poszukiwania
param_space = {
    'n_neighbors': (1, 10)  # zakres możliwych wartości liczby sąsiadów
}

# Inicjalizacja optymalizacji bayesowskiej
opt = BayesSearchCV(knn, param_space, n_iter=50, cv=5)

# Dopasowanie modelu do danych treningowych
opt.fit(X_train, y_train)

# Najlepsze znalezione parametry
best_params = opt.best_params_
print("Najlepsze parametry:", best_params)

# Predykcja dla danych testowych z wykorzystaniem najlepszych parametrów
y_pred = opt.predict(X_test)

# Dekodowanie etykiet kategorii
y_pred = label_encoder.inverse_transform(y_pred)

# Wyświetlenie wyników predykcji
for i in range(len(X_test)):
    print('Dane wejściowe:', X_test[i])
    print('Oczekiwana marka telefonu:', label_encoder.inverse_transform([y_test[i]]))
    print('Przewidziana marka telefonu:', y_pred[i])
    print()

# Ocena dokładności modelu
accuracy = opt.score(X_test, y_test)
print('Dokładność modelu:', accuracy)

# stwórz macierz pomyłek
cm = confusion_matrix(y_test, opt.predict(X_test))

# wyświetl macierz pomyłek w konsoli
print(cm)

#zsumuj wszystkie wartości w macierzy pomyłek
sum = np.sum(cm)
print(sum)

# wyświetl macierz pomyłek w postaci graficznej
plt.figure(figsize=(12, 12))
sns.heatmap(cm, annot=True, fmt=".0f", linewidths=.5, square=True, cmap='Blues_r')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
all_sample_title = 'Accuracy Score: {0}'.format(accuracy)
plt.title(all_sample_title, size=15)
plt.show()