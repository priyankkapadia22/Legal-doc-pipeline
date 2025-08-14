const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const db = new sqlite3.Database('./data/legal_docs.db');

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/api/cases', (req, res) => {
  const party = req.query.party || '';
  db.all(
    `SELECT * FROM cases WHERE party LIKE ? OR summary LIKE ?`,
    [`%${party}%`, `%${party}%`],
    (err, rows) => {
      if (err) {
        console.error('Database error:', err.message);
        return res.status(500).json({ error: 'Internal server error' });
      }

      const result = rows.map(row => ({
        party: row.party,
        case_number: row.case_number,
        date: row.date,
        summary: row.summary,
        ai_summary: row.ai_summary,
        matched_keyword: party
      }));

      res.json(result);
    }
  );
});

app.use((req, res) => {
  res.status(404).send('Route not found');
});

app.listen(3000, () => {
  console.log('API running on http://localhost:3000');
});