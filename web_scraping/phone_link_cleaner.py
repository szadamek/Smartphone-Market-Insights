import re

with open('phones_new.txt', 'r') as file:
    text = file.read()

clean_text = re.sub(r'VM\d+:\d+\s', '', text)

with open('phones_clean.txt', 'w') as file:
    file.write(clean_text)
