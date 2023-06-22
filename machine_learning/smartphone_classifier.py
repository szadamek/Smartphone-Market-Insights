import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import json
from sklearn.metrics import confusion_matrix, accuracy_score
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Wczytanie danych z pliku
with open('../web_scraping/phones_data_connected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Usuń telefony, które nie mają podanych parametrów
for phone in data:
    for param in ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']:
        try:
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
phone_names = []
for phone in data:
    if all([phone[param] is not None for param in
            ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora',
             'Marka telefonu', 'Model telefonu']]):
        X.append([phone[param] for param in
                  ['Szerokość', 'Wysokość', 'Głębokość', 'Waga', 'Częstotliwość procesora', 'Pojemność akumulatora']])
        # predykuj markę i model telefonu
        y.append(phone['Marka telefonu'])
        phone_names.append(f"{phone['Marka telefonu']} {phone['Model telefonu']}")

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test, phone_names_train, phone_names_test = train_test_split(X, y, phone_names,
                                                                                         test_size=0.2, random_state=42)

# Definicja modelu Drzewa decyzyjnego
decision_tree = DecisionTreeClassifier()

# Definicja modelu Random Forest
random_forest = RandomForestClassifier()

# Definicja modelu KNN
knn = KNeighborsClassifier(n_neighbors=1)

# ----------------------------------------------------------------------------------------------------------------------

# Sprawdzenie, czy istnieje zapisany model KNN
try:
    # Wczytanie wcześniej zapisanego modelu KNN
    knn = joblib.load("knn_model.pkl")
    print("Wczytano zapisany model KNN")
except FileNotFoundError:
    # Trenowanie modelu KNN
    start_time = time.time()
    knn.fit(X_train, y_train)
    end_time = time.time()
    print("Czas trenowania KNN:", end_time - start_time, "sekundy")

    # Zapisanie wytrenowanego modelu
    joblib.dump(knn, "knn_model.pkl")
    print("Zapisano wytrenowany model KNN")

# Predykcja na zbiorze testowym
y_pred_knn = knn.predict(X_test)

# Stwórz macierz pomyłek ale dla marki telefonu
cm_knn = confusion_matrix(y_test, y_pred_knn)
print("Macierz pomyłek (KNN):")
print(cm_knn)

# Utworzenie listy unikalnych etykiet
unique_labels = sorted(set(y_test))

cm_knn = np.delete(cm_knn, -14, axis=1)

# usuń ostatni wiersz z macierzy pomyłek
cm_knn = np.delete(cm_knn, -14, axis=0)

# Wizualizacja macierzy pomyłek z uwzględnieniem brakujących etykiet
plt.figure(figsize=(10, 8))
sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Blues')

# Dodanie nazw marek telefonów na wykres
tick_marks = [i + 0.5 for i in range(len(unique_labels))]
unique_labels = [label.replace(' ', '\n') for label in unique_labels]
plt.xticks(tick_marks, unique_labels, rotation=90, fontsize=8, ha='right')
plt.yticks(tick_marks, unique_labels, rotation=0, fontsize=8)

plt.title('Macierz pomyłek (KNN)')
plt.xlabel('Przewidziane etykiety')
plt.ylabel('Rzeczywiste etykiety')

plt.show()

# wskaźnik jakości modelu
accuracy_knn = accuracy_score(y_test, y_pred_knn)
print("Dokładność (KNN):", accuracy_knn)

# ----------------------------------------------------------------------------------------------------------------------

# Sprawdzenie, czy istnieje zapisany model Random Forest
try:
    # Wczytanie wcześniej zapisanego modelu Random Forest
    random_forest = joblib.load("random_forest_model.pkl")
    print("Wczytano zapisany model Random Forest")
except FileNotFoundError:
    # Trenowanie modelu Random Forest
    start_time = time.time()
    random_forest.fit(X_train, y_train)
    end_time = time.time()
    print("Czas trenowania Random Forest:", end_time - start_time, "sekundy")

    # Zapisanie wytrenowanego modelu
    joblib.dump(random_forest, "random_forest_model.pkl")
    print("Zapisano wytrenowany model Random Forest")

# Predykcja na zbiorze testowym
y_pred_rf = random_forest.predict(X_test)

# Stwórz macierz pomyłek ale dla marki telefonu
cm_rf = confusion_matrix(y_test, y_pred_rf)
print("Macierz pomyłek (Random Forest):")
print(cm_rf)

# Utworzenie listy unikalnych etykiet
unique_labels = sorted(set(y_test))

# cm_rf = np.delete(cm_rf, -14, axis=1)
#
# # usuń ostatni wiersz z macierzy pomyłek
# cm_rf = np.delete(cm_rf, -14, axis=0)

# Wizualizacja macierzy pomyłek z uwzględnieniem brakujących etykiet
plt.figure(figsize=(10, 8))
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues')

# Dodanie nazw marek telefonów na wykres
tick_marks = [i + 0.5 for i in range(len(unique_labels))]
unique_labels = [label.replace(' ', '\n') for label in unique_labels]
plt.xticks(tick_marks, unique_labels, rotation=90, fontsize=8, ha='right')
plt.yticks(tick_marks, unique_labels, rotation=0, fontsize=8)

plt.title('Macierz pomyłek (Random Forest)')
plt.xlabel('Przewidziane etykiety')
plt.ylabel('Rzeczywiste etykiety')

plt.show()

# wskaźnik jakości modelu
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print("Dokładność (Random Forest):", accuracy_rf)

# ----------------------------------------------------------------------------------------------------------------------

# Sprawdzenie, czy istnieje zapisany model Drzewa decyzyjnego
try:
    # Wczytanie wcześniej zapisanego modelu Drzewa decyzyjnego
    decision_tree = joblib.load("decision_tree_model.pkl")
    print("Wczytano zapisany model Drzewo decyzyjne")
except FileNotFoundError:
    # Trenowanie modelu Drzewa decyzyjnego
    start_time = time.time()
    decision_tree.fit(X_train, y_train)
    end_time = time.time()
    print("Czas trenowania Drzewo decyzyjne:", end_time - start_time, "sekundy")

    # Zapisanie wytrenowanego modelu
    joblib.dump(decision_tree, "decision_tree_model.pkl")
    print("Zapisano wytrenowany model Drzewo decyzyjne")

# Predykcja na zbiorze testowym
y_pred_dt = decision_tree.predict(X_test)

# Stwórz macierz pomyłek ale dla marki telefonu
cm_dt = confusion_matrix(y_test, y_pred_dt)
print("Macierz pomyłek (Drzewo decyzyjne):")
print(cm_dt)

# Utworzenie listy unikalnych etykiet
unique_labels = sorted(set(y_test))

cm_dt = np.delete(cm_dt, -14, axis=1)
cm_dt = np.delete(cm_dt, -12, axis=1)

# usuń ostatni wiersz z macierzy pomyłek
cm_dt = np.delete(cm_dt, -14, axis=0)
cm_dt = np.delete(cm_dt, -12, axis=0)

# Wizualizacja macierzy pomyłek z uwzględnieniem brakujących etykiet
plt.figure(figsize=(10, 8))
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues')

# Dodanie nazw marek telefonów na wykres
tick_marks = [i + 0.5 for i in range(len(unique_labels))]
unique_labels = [label.replace(' ', '\n') for label in unique_labels]
plt.xticks(tick_marks, unique_labels, rotation=90, fontsize=8, ha='right')
plt.yticks(tick_marks, unique_labels, rotation=0, fontsize=8)

plt.title('Macierz pomyłek (Drzewo decyzyjne)')
plt.xlabel('Przewidziane etykiety')
plt.ylabel('Rzeczywiste etykiety')

plt.show()

# wskaźnik jakości modelu
accuracy_dt = accuracy_score(y_test, y_pred_dt)
print("Dokładność (Drzewo decyzyjne):", accuracy_dt)
