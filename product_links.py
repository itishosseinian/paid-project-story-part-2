import requests
from bs4 import BeautifulSoup
import json


url = "https://www.construct-online.ch/65-menuiserie-et-bois?page=1"

with open('all_urls.json','r') as file:
    data = json.load(file)

results = {}
    
headers = {
    'User-Agent': 'Mozilla/5.3 (Windows NT 10.0; Win64; x64) AppleWebKit/534.36 (KHTML, like Gecko) Chrome/93.0.4606.71 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.construct-online.ch/'
}


for category,data in data.items():
    product_links = []

    pagination_links = data['pagination']
    print(f'working on {category} category')

    for page_url in pagination_links:

        print(f'Requesting to {page_url}')
        response = requests.get(url, headers=headers)

        if response.status_code ==200:
            soup = BeautifulSoup(response.text,'html.parser')
            products = soup.select('a.thumbnail.product-thumbnail')

            for product in products:
                product_links.append(product['href'])

            print(f'{len(products)} extracted')

        else:
            print(f'failed {response.status_code}')

    results[category] = {
        'url': data['url'],
        'pagination': data['pagination'],
        'product_links': product_links
    }
    
with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)    