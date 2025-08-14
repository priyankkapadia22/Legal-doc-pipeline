import os
import sqlite3
from transformers import pipeline
from pdfplumber import open as open_pdf
from langdetect import detect
from datetime import datetime

PDF_DIR = 'pdfs'
DB_PATH = 'api/data/legal_docs.db'
KEYWORDS = ['Wipro', 'Infosys', 'TCS']

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text(pdf_path):
    with open_pdf(pdf_path) as pdf:
        return '\n'.join(page.extract_text() or '' for page in pdf.pages)

def generate_summary(text):
    if len(text) < 100:
        return "Text too short to summarize."
    try:
        return summarizer(text[:1000], max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    except Exception as e:
        return f"Error: {str(e)}"

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'unknown'

def extract_metadata(filename, text):
    title = filename
    date = filename[:10] if filename[:10].isdigit() else datetime.today().strftime('%Y-%m-%d')
    matched = next((kw for kw in KEYWORDS if kw.lower() in text.lower()), None)
    snippet = text[:300].replace('\n', ' ')
    summary = generate_summary(text)
    return title, date, matched or 'None', snippet, summary

def store_in_db(records):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party TEXT,
            case_number TEXT,
            date TEXT,
            summary TEXT,
            ai_summary TEXT
        )
    ''')
    for record in records:
        cursor.execute('''
            INSERT INTO cases (party, case_number, date, summary, ai_summary)
            VALUES (?, ?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

records = []
for file in os.listdir(PDF_DIR):
    if file.endswith('.pdf'):
        path = os.path.join(PDF_DIR, file)
        raw_text = extract_text(path)
        lang = detect_language(raw_text)
       
        title, date, keyword, snippet, ai_summary = extract_metadata(file, raw_text)
        records.append((keyword or 'None', title, date, snippet, ai_summary))

store_in_db(records)
print(f"Processed {len(records)} PDFs and stored in DB.")