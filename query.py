import sqlite3

def query_party(party):
    conn = sqlite3.connect('data/legal_docs.db')
    c = conn.cursor()
    c.execute("SELECT title, date, keywords, snippet FROM documents WHERE keywords LIKE ? OR text LIKE ?", 
              (f'%{party}%', f'%{party}%'))
    results = c.fetchall()
    for r in results:
        print(f"\n📄 {r[0]} | 🗓️ {r[1]}\n🔍 Keywords: {r[2]}\n📝 Snippet: {r[3]}\n")

if __name__ == "__main__":
    party = input("Enter party name to search: ")
    query_party(party)