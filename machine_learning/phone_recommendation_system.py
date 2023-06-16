import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_processing.data_processing_file import remove_units, remove_phones_without_param

# Wczytaj dane z pliku JSON
with open('../web_scraping/phones_data_connected.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Usuń telefony, które nie mają podanych parametrów
data = remove_phones_without_param(data, 'Rodzaj wyświetlacza')
data = remove_phones_without_param(data, 'Rozdzielczość ekranu (px)')
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

# Usuń jednostki z parametrów liczbowych
data = remove_units(data, ['Rozdzielczość aparatu tylnego', 'Pojemność akumulatora', 'Pamięć RAM', 'Wbudowana pamięć', 'Waga', 'Wysokość',
                           'Częstotliwość procesora', 'Rozdzielczość ekranu (px)', 'Rozdzielczość aparatu przedniego', 'Szerokość',
                           'Gęstość pikseli'])

# Wylosuj 5 ofert ostatnich zakupów telefonów marki Samsung
recent_purchases = random.sample([phone for phone in data if phone['Marka telefonu'] == 'Samsung'], 5)
print("Ostatnie zakupy:")
for zakup in recent_purchases:
    print(f"- {zakup['Marka telefonu']} {zakup['Model telefonu']}")
print()

# Przygotuj listy cech telefonów
marki = []
modele = []
cechy = []

for telefon in data:
    marki.append(telefon['Marka telefonu'])
    modele.append(telefon['Model telefonu'])
    cechy.append(' '.join(
        [str(telefon['Marka telefonu']), str(telefon['Cena']), str(telefon['Rodzaj wyświetlacza']), str(telefon['Rozdzielczość ekranu (px)']),
         str(telefon['Rozdzielczość aparatu tylnego']), str(telefon['Pojemność akumulatora']),
         str(telefon['Pamięć RAM']),
         str(telefon['Wbudowana pamięć']), str(telefon['Waga']), str(telefon['Wysokość']),
         str(telefon['Częstotliwość procesora']), str(telefon['Marka telefonu']), str(telefon['Rozdzielczość aparatu przedniego']),
         str(telefon['Szerokość']), str(telefon['Gęstość pikseli'])]))  # Dodaj cechy telefonu do listy cechy

    modele.append(telefon['Marka telefonu'] + ' ' + telefon['Model telefonu'])  # Dodaj markę i model do listy modele

# Utwórz macierz cech telefonów
vectorizer = CountVectorizer().fit_transform(cechy)
cechy_matrix = vectorizer.toarray()

# Oblicz podobieństwo kosinusowe między cechami telefonów
similarities = cosine_similarity(cechy_matrix)

# Funkcja do zwracania rekomendacji
def recommend(telefon, n=3):
    index = modele.index(telefon['Model telefonu'])
    similarity_scores = list(enumerate(similarities[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_scores = similarity_scores[1:n+1]
    recommended_indices = [score[0] for score in top_scores]

    # Wybierz różne modele telefonów jako rekomendacje
    recommended_telefony = []
    added_models = set()
    for i in recommended_indices:
        if data[i]['Model telefonu'] not in added_models and data[i]['Model telefonu'] != telefon['Model telefonu']:
            recommended_telefony.append(data[i])
            added_models.add(data[i]['Model telefonu'])
            if len(recommended_telefony) == n:
                break

    # Jeśli nie ma żadnych rekomendacji, dodaj losowe telefony
    if len(recommended_telefony) == 0:
        random_telefony = random.sample(data, n)
        recommended_telefony.extend(random_telefony)

    return recommended_telefony


def evaluate_recommendation(original_phone, recommended_phones):
    original_brand = original_phone['Marka telefonu']
    original_model = original_phone['Model telefonu']

    # Pobierz parametry oryginalnego telefonu
    original_params = {
        'Rodzaj wyświetlacza': original_phone['Rodzaj wyświetlacza'],
        'Rozdzielczość ekranu (px)': original_phone['Rozdzielczość ekranu (px)'],
        'Rozdzielczość aparatu tylnego': original_phone['Rozdzielczość aparatu tylnego'],
        'Pojemność akumulatora': original_phone['Pojemność akumulatora'],
        'Pamięć RAM': original_phone['Pamięć RAM'],
        'Wbudowana pamięć': original_phone['Wbudowana pamięć'],
        'Waga': original_phone['Waga'],
        'Wysokość': original_phone['Wysokość'],
        'Szerokość': original_phone['Szerokość'],
        'Częstotliwość procesora': original_phone['Częstotliwość procesora'],
        'Rozdzielczość aparatu przedniego': original_phone['Rozdzielczość aparatu przedniego'],
        'Gęstość pikseli': original_phone['Gęstość pikseli'],
        'Cena': original_phone['Cena']
    }

    # Ocena jakości rekomendacji dla każdego zarekomendowanego telefonu
    scores = []
    for recommended_phone in recommended_phones:
        recommended_brand = recommended_phone['Marka telefonu']
        recommended_model = recommended_phone['Model telefonu']

        # Pobierz parametry zarekomendowanego telefonu
        recommended_params = {
            'Rodzaj wyświetlacza': recommended_phone['Rodzaj wyświetlacza'],
            'Rozdzielczość ekranu (px)': recommended_phone['Rozdzielczość ekranu (px)'],
            'Rozdzielczość aparatu tylnego': recommended_phone['Rozdzielczość aparatu tylnego'],
            'Pojemność akumulatora': recommended_phone['Pojemność akumulatora'],
            'Pamięć RAM': recommended_phone['Pamięć RAM'],
            'Wbudowana pamięć': recommended_phone['Wbudowana pamięć'],
            'Waga': recommended_phone['Waga'],
            'Wysokość': recommended_phone['Wysokość'],
            'Szerokość': recommended_phone['Szerokość'],
            'Częstotliwość procesora': recommended_phone['Częstotliwość procesora'],
            'Rozdzielczość aparatu przedniego': recommended_phone['Rozdzielczość aparatu przedniego'],
            'Gęstość pikseli': recommended_phone['Gęstość pikseli'],
            'Cena': recommended_phone['Cena']
        }

        # Liczba wspólnych parametrów między oryginalnym a zarekomendowanym telefonem
        common_params = sum(1 for param in original_params if original_params[param] == recommended_params[param])

        # Ocena jakości rekomendacji
        score = common_params / len(original_params)
        scores.append(score)

        print(f"Ocena rekomendacji dla telefonu {recommended_brand} {recommended_model}: {score}")

    # Średnia ocen jakości rekomendacji
    average_score = sum(scores) / len(scores)

    print(f"Średnia ocena jakości rekomendacji: {average_score}")
    return average_score


# Przykładowe użycie oceny jakości rekomendacji
for zakup in recent_purchases:
    rekomendacje = recommend(zakup, n=3)
    print(f"Rekomendacje dla telefonu {zakup['Marka telefonu']} {zakup['Model telefonu']}:")
    print("Parametry oferty wylosowanej:")
    print(zakup)
    print("Parametry zarekomendowanej oferty:")
    for telefon in rekomendacje:
        print(telefon)
    evaluate_recommendation(zakup, rekomendacje)
    print()

