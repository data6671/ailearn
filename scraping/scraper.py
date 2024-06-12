import requests
from bs4 import BeautifulSoup
import json
import unicodedata

def get_webpage(url):
    base_link = 'https://cojestgrane.pl' 
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    event_elements = soup.select('li')
    
    events = []
    for event_element in event_elements:
        event_html = str(event_element)
        event_text = event_element.get_text(strip=False)
        event_text = unicodedata.normalize('NFKD', event_text).encode('latin-1', 'ignore').decode('latin-1')
    
        event_soup = BeautifulSoup(event_html, 'html.parser')
        a = event_soup.select_one('li a')['href']
        title_elements = event_soup.select('li h1, li h2, li h3, li h4, li h5')
        titles = [title.get_text(strip=True) for title in title_elements]
        title = unicodedata.normalize('NFKD', titles[0]).encode('latin-1', 'ignore').decode('latin-1')
    
        new_link = base_link + a
        response = requests.get(new_link)
        new_html = response.text
    
        new_soup = BeautifulSoup(new_html, 'html.parser')
        detail_div = new_soup.find('div', id='details')
        detail_text = detail_div.get_text(strip=False) if detail_div else ''
        detail_text = unicodedata.normalize('NFKD', detail_text).encode('latin-1', 'ignore').decode('latin-1')
    
        ev_date = new_soup.find('time')['datetime']
        ev_time = new_soup.find('div', class_='ui-hours').text.strip()
        
        name = new_soup.find('span', itemprop='name', attrs={'class': None}).text.strip()
        adres = new_soup.find(attrs={"itemprop": "address"}).text.strip()
        place = new_soup.find(attrs={"itemprop": "addressLocality"}).text.strip()
        event_place = f'{name}\n{adres}\n{place}'
        event_place = unicodedata.normalize('NFKD', event_place).encode('latin-1', 'ignore').decode('latin-1')
    
        event_map_link = base_link + new_soup.find(itemprop='map')['href']
        
        event = {
            'ev_text': event_text,
            'ev_place': event_place,
            'ev_map': event_map_link,
            'ev_title': title,
            'ev_link': new_link,
            'ev_details': detail_text,
            'ev_date': ev_date,
            'ev_time': ev_time
        }
        events.append(event)

    return events

url = 'https://cojestgrane.pl/polska/slaskie/jest/7'
result = json.dumps(get_webpage(url), indent=2)
print(result)
