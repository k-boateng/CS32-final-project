import sqlite3
import threading
from datetime import datetime

class Message:
    def __init__(self, text, timestamp=None):
        self.text = text
        self.timestamp = timestamp or datetime.now().isoformat()

    def __repr__(self):
        return f"<Message {self.timestamp}: {self.text}>"

class MessageDatabase:
    def __init__(self, db_path, check_same_thread=True):
        self.lock = threading.Lock() #prevents different threads from access the same db file which may cause errors
        self.conn = sqlite3.connect(db_path, check_same_thread=check_same_thread)
        self._create_table()
        
    def _create_table(self):
        with self.lock:
            with self.conn:
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                ''')

    def save_message(self, message):
        with self.lock:
            with self.conn:
                self.conn.execute(
                    'INSERT INTO messages (text, timestamp) VALUES (?, ?)',
                    (message.text, message.timestamp)
                )

    #loads all messages between you and the friend from the dtabase file
    def get_all_messages(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('SELECT text, timestamp FROM messages ORDER BY id')
            return [Message(text=row[0], timestamp=row[1]) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()
