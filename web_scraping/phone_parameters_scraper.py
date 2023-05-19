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

        params_selector = 'body > div.main-wrapper > div > div > div > div:nth-child(7) > div > div > div:nth-child(4) > div > div > div.mpof_ki.msub_k4.myre_zn.mp7g_oh._9491e_bNo44.mr3m_1.mjyo_6x.gel0f.g69b4.g1wnk.g1s2l.mh36_0.mvrt_0.mvrt_8_m > div > div:nth-child(3) > div > div > div:nth-child(1) > div > div > div > div > div > div > div > div > div > div > table > tbody > tr'
        params_tr = soup.select(params_selector)
        params = {}
        for param in params_tr:
            key = param.select_one('td:nth-child(1)').text.strip()
            value = param.select_one('td:nth-child(2)').text.strip()
            params[key] = value

        print(params)

        time.sleep(5)
