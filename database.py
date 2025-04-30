import sqlite3
from datetime import datetime
from pathlib import Path

class Message:
    def __init__(self, text, timestamp=None):
        self.text = text
        self.timestamp = timestamp or datetime.now().isoformat()

    def __repr__(self):
        return f"<Message {self.timestamp}: {self.text}>"

class MessageDatabase:
    def __init__(self, db_path):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')

    def save_message(self, message: Message):
        with self.conn:
            self.conn.execute('INSERT INTO messages (text, timestamp) VALUES (?, ?)',
                              (message.text, message.timestamp))

    def get_all_messages(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT text, timestamp FROM messages ORDER BY id')
        rows = cursor.fetchall()
        return [Message(text=row[0], timestamp=row[1]) for row in rows]

    def close(self):
        self.conn.close()
