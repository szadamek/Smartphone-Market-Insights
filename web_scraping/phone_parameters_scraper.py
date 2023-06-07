import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import os
from data_processing.data_processing_file import remove_comma_from_price


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
        print(response.status_code)

    return response


def send_request(url):
    # Run hello world in JS and return result
    result = driver.execute_async_script("""
    function makeRequest(url, headers, callback) {
      const xhr = new XMLHttpRequest();

      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            const response = xhr.responseText;
            callback(response);
          } else {
            console.error('Error making the request. Status:', xhr.status);
            callback(null);
          }
        }
      };

      xhr.open('GET', url, true);

      for (const header in headers) {
        xhr.setRequestHeader(header, headers[header]);
      }

      xhr.send();
    }

    function handleResponse(response) {
        if (response) {
        console.log(response);
        // Process the response content as needed
        } else {
        console.error('Failed to get response');
        }
    }

    function sendRequest() {
        return new Promise(function(resolve, reject) {
            const url = '""" + url + """';
            const headers = {
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
            };

            makeRequest(url, headers, function(resp) {
                console.log(resp);
                resolve(resp);
            });
        });
    }


    var callback = arguments[arguments.length - 1];  // Last argument is the callback function

    sendRequest().then(function (value) {
        callback(value);  // Pass the result to the callback
    });
    """)

    return json.loads(result)


if __name__ == '__main__':
    # Set up Chrome driver
    chrome_driver_path = 'C:/TestFiles/chromedriver.exe'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    with open('phones.txt', 'r', encoding='utf-8') as f:
        phones = f.readlines()

    phones = [phone.strip() for phone in phones]

    for phone in phones:
        base_url = phone
        print(f'Phone: {base_url}')
        html = get_html_by_viewsource(base_url)
        soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(str(soup), 'html.parser')
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

        params_price_selector = 'body > div.main-wrapper > div:nth-child(7) > div > div > div:nth-child(7) > div > div > div > div > div > div.mpof_ki.msub_k4.myre_zn.mp7g_oh._9491e_bNo44.mr3m_1.mjyo_6x.gel0f.ggz4y.g1gsr.g1s2l.mh36_0.mh36_8_m.mg9e_16.mg9e_0_m > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div > div > div > div > div.msts_pt > div > div > div > span:nth-child(1)'
        params_price = soup.select_one(params_price_selector).text.strip()
        params_price = remove_comma_from_price(params_price)
        params['Cena'] = params_price

        view_box_json = send_request(base_url)

        view_box_html = view_box_json['htmlString']
        view_box_soup = BeautifulSoup(view_box_html, 'html.parser')
        # For debugging and testing selectors in Chrome
        with open('test_view_box.html', 'w', encoding='utf-8') as f:
            f.write(str(view_box_soup))

        view_box_html_selector = 'tr.mlkp_ag'
        params_tr = view_box_soup.select(view_box_html_selector)
        for param in params_tr:
            key = param.select_one('td:nth-child(1)').text.strip()
            value = param.select_one('td:nth-child(2)').text.strip()
            params[key] = value

        print(params)
        params['url'] = base_url

        # Save data to JSON file, appending new data
        # jezeli plik jest pusty
        if os.stat('phones_data_new.json').st_size == 0:
            with open('phones_data_new.json', 'a', encoding='utf-8') as f:
                json.dump([params], f, ensure_ascii=False)
        else:
            with open('phones_data_new.json', 'r+', encoding='utf-8') as f:
                # Load data from JSON file
                data = json.load(f)
                # Append new data to JSON file
                data.append(params)
                # Go to the beginning of the file
                f.seek(0)
                # Write data to the file
                json.dump(data, f, ensure_ascii=False)

        # usuń link z pliku phones.txt poprzez usunięcie linii znajdującej się najwyżej
        with open('phones.txt', 'r', encoding='utf-8') as fin:
            data = fin.read().splitlines(True)
        with open('phones.txt', 'w', encoding='utf-8') as fout:
            fout.writelines(data[1:])

        time.sleep(3)
