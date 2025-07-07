import sqlite3

conn = sqlite3.connect('spam_guard.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS spam_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    user_id INTEGER,
    message TEXT,
    action TEXT,
    log_time TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS spam_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE NOT NULL
)
''')

# Insert default spam keywords
keywords = [
    ('free',), ('crypto',), ('join now',), ('click here',),
    ('buy now',), ('earn money',)
]

cursor.executemany("INSERT OR IGNORE INTO spam_keywords (keyword) VALUES (?)", keywords)

conn.commit()
conn.close()
