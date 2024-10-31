import json

import requests
from bs4 import BeautifulSoup


def get_quote(url):
    quotes = []
    base_url = url

    while url:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        for quote in soup.find_all(class_='quote'):
            text = quote.find(class_='text').get_text()
            author = quote.find(class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all(class_='tag')]

            quotes.append(
                {'text': text,
                 'author': author,
                 'tags': tags}
            )

        next_page = soup.find(class_='next')

        if next_page:
            url = base_url + next_page.find('a')['href']
        else:
            url = None

    return quotes


def save_quotes_to_json(quotes):
    with open('quotes.json', 'w', encoding='utf-8') as file:
        json.dump(quotes, file, ensure_ascii=False, indent=3)


if __name__ == '__main__':
    url = 'https://quotes.toscrape.com/'
    quotes = get_quote(url)
    save_quotes_to_json(quotes)
