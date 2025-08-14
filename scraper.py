import requests
from bs4 import BeautifulSoup
from config import SOURCE_URL

def scrape_pdf_links():
    res = requests.get(SOURCE_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    return links