import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_html_page(url):
    driver.get(url)
    html = driver.page_source
    return html


def get_html_by_viewsource(url):
    html = get_html_page('view-source:' + url)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.text


if __name__ == '__main__':
    # Set up Chrome driver
    chrome_driver_path = 'C:/TestFiles/chromedriver.exe'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    base_url = 'https://allegro.pl/kategoria/smartfony-i-telefony-komorkowe-165'
    phones_file = 'phones.txt'

    # Getting phones urls from phones.txt as an array
    phones = []

    if os.path.isfile(phones_file):
        with open(phones_file, 'r', encoding='utf-8') as f:
            for line in f:
                phones.append(line.strip())
    else:
        print('File not found. Creating new file.')
        open(phones_file, 'w', encoding='utf-8').close()

    total_new_phones = 0
    page_num = 1
    while True:
        url = f'{base_url}?p={page_num}'
        print(f'Strona {page_num}: {url}')
        html = get_html_by_viewsource(url)
        soup = BeautifulSoup(html, 'html.parser')

        # For debugging and testing selectors in Chrome
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))

        new_phones = 0
        phone_selectors = '#search-results > div > div > div > div > div > div > section > article > div > div > div.mpof_ki.myre_zn.mh36_8.mjyo_6x._6a66d_5o-oq > div.m7er_k4.mj7a_4 > h2 > a'
        for a in soup.select(phone_selectors):
            print("Found the URL:", a['href'])
            if a['href'] not in phones:
                phones.append(a['href'])
                new_phones += 1
                total_new_phones += 1

        if new_phones == 0:
            # No new phones found on this page, exit the loop
            break

        # Saving phones urls to phones.txt
        with open(phones_file, 'w', encoding='utf-8') as f:
            for phone in phones:
                f.write(phone + '\n')

        print(f'Added {new_phones} new phones to {phones_file}')

        page_num += 1

        # Generate random sleep time between requests (1-3 seconds)
        sleep_time = random.uniform(3, 8)
        time.sleep(sleep_time)

    print(f'Total {total_new_phones} new phones added')