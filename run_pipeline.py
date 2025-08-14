from scraper import scrape_pdf_links
from downloader import download_and_extract
from processor import extract_metadata
from database import init_db, insert_document

def run():
    links = scrape_pdf_links()
    conn = init_db()
    for url in links:
        try:
            filename, text = download_and_extract(url)
            metadata = extract_metadata(filename, text)
            insert_document(conn, metadata)
            print(f"Processed: {filename}")
        except Exception as e:
            print(f"Error with {url}: {e}")

if __name__ == "__main__":
    run()