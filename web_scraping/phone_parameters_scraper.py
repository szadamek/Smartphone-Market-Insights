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

    with open('phones_links.txt', 'r', encoding='utf-8') as f:
        phones = f.readlines()

    phones = [phone.strip() for phone in phones]

    phone_parameters = []
    for phone in phones:
        base_url = phone
        print(f'Phone: {base_url}')
        html = get_html_by_viewsource(base_url)
        soup = BeautifulSoup(html, 'html.parser')
        # For debugging and testing selectors in Chrome
        with open('test_parameters.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))

        phone_selector = 'body > div.main-wrapper > div:nth-child(7) > div > div > div:nth-child(7) > div > div > div:nth-child(2)'
        print(soup.select(phone_selector))

        time.sleep(10)
