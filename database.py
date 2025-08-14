import sqlite3

def init_db():
    conn = sqlite3.connect('data/legal_docs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS documents (
        title TEXT, date TEXT, keywords TEXT, snippet TEXT, text TEXT
    )''')
    conn.commit()
    return conn

def insert_document(conn, metadata):
    c = conn.cursor()
    c.execute('INSERT INTO documents VALUES (?, ?, ?, ?, ?)', (
        metadata['title'], metadata['date'], metadata['keywords'],
        metadata['snippet'], metadata['text']
    ))
    conn.commit()