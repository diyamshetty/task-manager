import sqlite3
import datetime
from datetime import date, timedelta

# Fix Python 3.12 date warning
sqlite3.register_adapter(datetime.date, lambda d: d.isoformat())
sqlite3.register_converter("DATE", lambda s: datetime.date.fromisoformat(s.decode()))

# Connect to SQLite (creates DB if it doesn't exist)
conn = sqlite3.connect("tasks.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()

# Drop old tables (to avoid schema conflicts)
cursor.execute("DROP TABLE IF EXISTS tasks;")
cursor.execute("DROP TABLE IF EXISTS users;")

# Create tables
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);
''')

cursor.execute('''
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('To Do','In Progress','Done')) DEFAULT 'To Do',
    priority TEXT CHECK(priority IN ('Low','Medium','High')) DEFAULT 'Medium',
    due_date DATE,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
''')

# Insert sample users
users = [
    ("Alice", "alice@example.com"),
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com")
]
cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)

# Fetch user IDs
cursor.execute("SELECT user_id, name FROM users;")
user_map = {name: uid for uid, name in cursor.fetchall()}

# Today's date
today = date.today()

# Insert sample tasks
tasks = [
    ("Prepare Report", "Monthly sales report", "To Do", "High", today + timedelta(days=5), user_map["Alice"]),
    ("Database Backup", "Weekly backup of production DB", "In Progress", "Medium", today + timedelta(days=2), user_map["Bob"]),
    ("Team Meeting", "Discuss Q3 strategy", "Done", "Low", today - timedelta(days=1), user_map["Charlie"]),
    ("Bug Fix", "Resolve login issue", "To Do", "High", today + timedelta(days=1), user_map["Alice"]),
    ("Code Review", "Review PR #42", "Done", "Medium", today - timedelta(days=3), user_map["Bob"]),
    ("Prepare Presentation", "Slides for client meeting", "To Do", "High", today + timedelta(days=7), user_map["Charlie"])
]
cursor.executemany("""
INSERT INTO tasks (title, description, status, priority, due_date, user_id)
VALUES (?, ?, ?, ?, ?, ?)
""", tasks)

conn.commit()
conn.close()

print("✅ Sample database 'tasks.db' created & populated successfully!")
print("Now run: python task_tracker.py")

