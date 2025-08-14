import requests, os
import pdfplumber

def download_and_extract(url, save_dir='data/pdfs'):
    os.makedirs(save_dir, exist_ok=True)
    filename = url.split('/')[-1]
    filepath = os.path.join(save_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(requests.get(url).content)

    with pdfplumber.open(filepath) as pdf:
        text = ''.join(page.extract_text() or '' for page in pdf.pages)
    return filename, text