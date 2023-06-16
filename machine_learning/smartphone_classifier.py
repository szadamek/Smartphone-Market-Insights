from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json
from skopt import BayesSearchCV
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Wczytanie danych z pliku
with open('../web_scraping/phones_data_connected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Usuń telefony, które nie mają podanych parametrów
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
# usuń telefony, które nie mają w ogóle parametru model telefonu
data = [phone for phone in data if 'Model telefonu' in phone]

# Przygotowanie danych treningowych
X = []
y = []
# weź tylko te telefony które mają wszystkie parametry kompletne włącznie z marką telefonu
for phone in data:
    if all([phone[param] is not None for param in ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora', 'Marka telefonu', 'Model telefonu']]):
        X.append([phone[param] for param in ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']])
        y.append(phone['Marka telefonu'] + ' ' + phone['Model telefonu'])

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definicja modelu Drzewa decyzyjnego
decision_tree = DecisionTreeClassifier()

# Definicja modelu Gradient Boosting
gradient_boosting = GradientBoostingClassifier()

# Definicja przestrzeni poszukiwania
param_space = {
    'max_depth': (1, 10),  # zakres możliwych wartości maksymalnej głębokości dla drzewa decyzyjnego
    'learning_rate': (0.001, 1.0, 'log-uniform')  # zakres możliwych wartości współczynnika uczenia dla Gradient Boosting
}

# Definicja obiektu BayesSearchCV
opt = BayesSearchCV(
    gradient_boosting,  # model do strojenia
    param_space,  # przestrzeń poszukiwania
    n_iter=50,  # liczba iteracji
    random_state=42
)

# Strojenie hiperparametrów
opt.fit(X_train, y_train)

# Najlepsze znalezione parametry
best_params = opt.best_params_
print("Najlepsze parametry:", best_params)

# Dostosowanie modelu z najlepszymi parametrami
gradient_boosting_best = GradientBoostingClassifier(**best_params)

# Trenowanie modelu Gradient Boosting z najlepszymi parametrami
gradient_boosting_best.fit(X_train, y_train)

# Predykcja na zbiorze testowym
y_pred_gb = gradient_boosting_best.predict(X_test)

# Ewaluacja modelu Gradient Boosting
cm_gb = confusion_matrix(y_test, y_pred_gb)
print("Macierz pomyłek (Gradient Boosting):")
print(cm_gb)

# Trenowanie modelu Drzewa decyzyjnego
decision_tree.fit(X_train, y_train)

# Predykcja na zbiorze testowym
y_pred_dt = decision_tree.predict(X_test)

# Ewaluacja modelu Drzewa decyzyjnego
cm_dt = confusion_matrix(y_test, y_pred_dt)
print("Macierz pomyłek (Drzewo decyzyjne):")
print(cm_dt)
