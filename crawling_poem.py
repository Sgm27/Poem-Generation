import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) '\
    'Chrome/75.0.3770.80 Safari/537.36'
}

samples = []

def process_for_page(url):
    reponse = requests.get(url, headers=headers)
    soup = BeautifulSoup(reponse.text, 'lxml')
    list_poem = soup.find_all('div', class_='list-item')

    for poem in list_poem:
        poem_url = 'https://www.thivien.net' + poem.find('a')['href']
        poem_page = requests.get(poem_url, headers=headers)
        poem_soup = BeautifulSoup(poem_page.text, 'lxml')
        content = poem_soup.find('div', class_='poem-content')
        content = content.find('p')
        content = content.decode_contents()
        content = content.replace('<br/>', '\n')

        header = poem_soup.find(class_ = 'page-header')
        title = header.find('h1').text

        sample = {
            'content': content,
            'title': title
        }

        print(title)

        samples.append(sample)

for poem_type in range(1, 25):
    for page in range(1, 11):
        url = f'https://www.thivien.net/searchpoem.php?PoemType={poem_type}&ViewType=1&Country=2&Page={page}'
        try:
            process_for_page(url)
        except:
            pass

df = pd.DataFrame(samples)
df.to_csv('poems.csv', index=True)


    
    