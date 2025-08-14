const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const fs = require('fs');
const dbDir = path.join(__dirname, '../data');
if (!fs.existsSync(dbDir)) fs.mkdirSync(dbDir);

const dbPath = path.join(dbDir, 'legal_docs.db');
const db = new sqlite3.Database(dbPath);

db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    party TEXT NOT NULL,
    case_number TEXT UNIQUE NOT NULL,
    date TEXT,
    summary TEXT
  )`);

  const stmt = db.prepare(`INSERT INTO cases (party, case_number, date, summary) VALUES (?, ?, ?, ?)`);
  stmt.run('Wipro Ltd.', 'CIV-2023-001', '2023-06-15', 'Contract dispute over service delivery timelines.');
  stmt.run('Infosys Ltd.', 'CIV-2023-002', '2023-07-01', 'IP infringement claim regarding software module.');
  stmt.run('TCS Ltd.', 'CIV-2023-003', '2023-07-20', 'Employment termination challenge.');
  stmt.finalize();
});

db.close(() => {
  console.log('Database seeded successfully at:', dbPath);
});