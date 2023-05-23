import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import subprocess
import requests


def get_html_page(url):
    driver.get(url)
    html = driver.page_source
    return html


def get_html_by_viewsource(url):
    html = get_html_page('view-source:' + url)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.text


def handle_response(response):
    if response:
        print(response.json())  # Przetwarzaj odpowiedź tak, jak jest to wymagane
    else:
        print('Failed to get response')

def send_request(url):
    headers = {
        'accept': 'application/vnd.opbox-web.subtree+json',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'dpr': '1',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Chromium";v="112.0.5615.138", "Google Chrome";v="112.0.5615.138", "Not:A-Brand";v="99.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'viewport-width': '1017',
        'x-box-id': 'LUo64bt1RQOuwIphdVaomw==sx2lrxHNQUG4Wa7QQbUK8g==4iJ4NQTRQsGK0YC-eOOwlg==',
        'x-view-id': '883a645a-5832-49ac-8824-93e78d55c745'
    }

    response = requests.get(url, headers=headers)
    handle_response(response)


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
        phone_parameters.append(params)

        send_request(base_url)

        print(params)



        time.sleep(5)
