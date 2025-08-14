import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Create Tables
# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
)
''')

# Tasks table with a foreign key referencing users
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT CHECK(priority IN ('High','Medium','Low')) DEFAULT 'Medium',
    status TEXT CHECK(status IN ('To Do','In Progress','Done')) DEFAULT 'To Do',
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')

# User Management 
def add_user():
    """Insert a new user into the users table"""
    name = input("Enter user name: ")
    email = input("Enter user email: ")
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    print(" User added successfully!")

def view_users():
    """Display all users"""
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)

#Task Management 
def add_task():
    """Insert a new task assigned to a user"""
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    priority = input("Priority (High/Medium/Low): ")
    due_date = input("Due date (YYYY-MM-DD): ")

    # Show available users to assign the task
    view_users()
    user_id = input("Enter user_id to assign this task: ")

    cursor.execute("""
        INSERT INTO tasks (title, description, priority, due_date, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, priority, due_date, user_id))
    conn.commit()
    print("✅ Task added successfully!")

def view_tasks():
    """View all tasks with assigned user's name using JOIN"""
    cursor.execute("""
        SELECT t.id, t.title, t.status, t.priority, t.due_date, u.name
        FROM tasks t
        JOIN users u ON t.user_id = u.user_id
    """)
    for row in cursor.fetchall():
        print(row)

def update_task():
    """Update task status"""
    task_id = input("Enter task ID to update: ")
    status = input("New status (To Do/In Progress/Done): ")
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    print("✅ Task updated!")

def delete_task():
    """Delete a task"""
    task_id = input("Enter task ID to delete: ")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print("🗑️ Task deleted!")

# Reports 
def report_tasks_by_user():
    """Count of tasks assigned to each user"""
    cursor.execute("""
        SELECT u.name, COUNT(*) AS task_count
        FROM tasks t
        JOIN users u ON t.user_id = u.user_id
        GROUP BY u.name
    """)
    for row in cursor.fetchall():
        print(row)

def report_completed_tasks():
    """Number of completed tasks per user"""
    cursor.execute("""
        SELECT u.name, COUNT(*) AS completed_tasks
        FROM tasks t
        JOIN users u ON t.user_id = u.user_id
        WHERE t.status = 'Done'
        GROUP BY u.name
    """)
    for row in cursor.fetchall():
        print(row)

def report_overdue_tasks():
    """Overdue tasks per user"""
    cursor.execute("""
        SELECT u.name, t.title, t.due_date
        FROM tasks t
        JOIN users u ON t.user_id = u.user_id
        WHERE t.due_date < DATE('now') AND t.status != 'Done'
    """)
    for row in cursor.fetchall():
        print(row)

# Menu Loop
while True:
    print("\n--- Task Tracking System ---")
    print("1. Add User")
    print("2. View Users")
    print("3. Add Task")
    print("4. View Tasks")
    print("5. Update Task Status")
    print("6. Delete Task")
    print("7. Report: Tasks by User")
    print("8. Report: Completed Tasks per User")
    print("9. Report: Overdue Tasks")
    print("10. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_user()
    elif choice == "2":
        view_users()
    elif choice == "3":
        add_task()
    elif choice == "4":
        view_tasks()
    elif choice == "5":
        update_task()
    elif choice == "6":
        delete_task()
    elif choice == "7":
        report_tasks_by_user()
    elif choice == "8":
        report_completed_tasks()
    elif choice == "9":
        report_overdue_tasks()
    elif choice == "10":
        break
    else:
        print("Invalid choice! Please try again.")

# Close DB connection
conn.close()

