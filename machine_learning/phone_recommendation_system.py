import json
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_processing.data_processing_file import remove_units, remove_phones_without_param

# Wczytaj dane z pliku JSON
with open('../web_scraping/phones_data_connected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Usuń telefony, które nie mają podanych parametrów
data = remove_phones_without_param(data, 'Rodzaj wyświetlacza')
data = remove_phones_without_param(data, 'Rozdzielczość aparatu tylnego')
data = remove_phones_without_param(data, 'Pojemność akumulatora')
data = remove_phones_without_param(data, 'Pamięć RAM')
data = remove_phones_without_param(data, 'Wbudowana pamięć')
data = remove_phones_without_param(data, 'Waga')
data = remove_phones_without_param(data, 'Wysokość')
data = remove_phones_without_param(data, 'Szerokość')
data = remove_phones_without_param(data, 'Marka telefonu')
data = remove_phones_without_param(data, 'Model telefonu')
data = remove_phones_without_param(data, 'Częstotliwość procesora')
data = remove_phones_without_param(data, 'Rozdzielczość aparatu przedniego')
data = remove_phones_without_param(data, 'Gęstość pikseli')
data = remove_phones_without_param(data, 'Cena')
print(f"Liczba telefonów po usunięciu tych bez podanych parametrów: {len(data)}")

# Usuń parametry które są inne niż te powyżej
required_keys = ['Rodzaj wyświetlacza', 'Rozdzielczość aparatu tylnego', 'Pojemność akumulatora', 'Pamięć RAM',
                 'Wbudowana pamięć', 'Waga', 'Wysokość', 'Szerokość', 'Marka telefonu', 'Model telefonu', 'Częstotliwość procesora',
                 'Rozdzielczość aparatu przedniego', 'Gęstość pikseli', 'Cena']
data = [{key: phone[key] for key in required_keys} for phone in data]

# Usuń jednostki z parametrów liczbowych
data = remove_units(data, ['Rozdzielczość aparatu tylnego', 'Pojemność akumulatora', 'Pamięć RAM', 'Wbudowana pamięć', 'Waga', 'Wysokość',
                           'Częstotliwość procesora', 'Rozdzielczość aparatu przedniego', 'Szerokość',
                           'Gęstość pikseli'])

# Weź tylko popularne marki telefonów
popular_brands = ['Samsung', 'Apple', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo', 'Realme', 'OnePlus', 'Motorola', 'Lenovo', 'LG', 'Sony', 'Nokia', 'HTC', 'Google']
data = [phone for phone in data if phone['Marka telefonu'] in popular_brands]
print(f"Liczba telefonów po usunięciu tych z niepopularnych marek: {len(data)}")

# Wylosowanie 3 telefonów
random.seed(42)
selected_phones = random.sample(data, 3)

# Przygotuj dane do trenowania modelu
descriptions = [
    ' '.join([str(phone[key]) for key in required_keys]) for phone in data
]

# Przygotowanie wektoryzera TF-IDF
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(descriptions)

# Przygotowanie wektora średniego dla wylosowanych telefonów
selected_vectors = vectorizer.transform([
    ' '.join([str(phone[key]) for key in required_keys]) for phone in selected_phones
])
average_vector = np.asarray(selected_vectors.mean(axis=0))

# Obliczenie podobieństwa kosinusowego między średnim wektorem a innymi telefonami
similarities = cosine_similarity(average_vector, vectors)

# Znalezienie najbardziej podobnego telefonu do średniego wektora, który jest innego modelu niż wylosowane telefony
most_similar_phone_index = similarities.argmax()
most_similar_phone = data[most_similar_phone_index]

while most_similar_phone['Model telefonu'] in [phone['Model telefonu'] for phone in selected_phones]:
    similarities[0, most_similar_phone_index] = 0  # Ustawienie podobieństwa do już wylosowanych telefonów na 0
    most_similar_phone_index = similarities.argmax()
    most_similar_phone = data[most_similar_phone_index]

# Wyświetlenie wyników
print('Wylosowane telefony:')
for phone in selected_phones:
    print(phone)
print('Najbardziej podobny telefon (inny model):')
print(most_similar_phone)

# Wykres podobieństwa kosinusowego
plt.figure(figsize=(12, 6))

# Posortuj telefony malejąco według wartości podobieństwa kosinusowego
sorted_indices = np.argsort(similarities[0])[::-1]
sorted_similarities = similarities[0, sorted_indices]
sorted_phones = [data[i]['Model telefonu'] for i in sorted_indices]

# Indeks telefonu rekomendowanego
recommended_index = sorted_phones.index(most_similar_phone['Model telefonu'])

# Wybierz 10 losowych telefonów spośród pozostałych
random_indices = random.sample(range(1, len(sorted_phones)), 10)
phones_to_display = [sorted_phones[i] for i in random_indices]
indices_to_display = [i for i in random_indices] + [recommended_index]
phones_to_display.append(sorted_phones[recommended_index])

plt.bar(range(len(sorted_similarities)), sorted_similarities, color='b')
plt.xlabel('Model telefonu')
plt.ylabel('Podobieństwo kosinusowe')
plt.title('Podobieństwo kosinusowe między średnim wektorem a telefonami (posortowane malejąco)')
plt.xticks(indices_to_display, phones_to_display, rotation=45, ha='right')
plt.tight_layout()
plt.show()
