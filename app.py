import psycopg2
import os
from datetime import datetime

def connect():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

def setup(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            goal TEXT NOT NULL,
            deadline DATE NOT NULL
        )
    """)
    conn.commit()
    cur.close()

def add_goal(conn, goal, deadline):
    cur = conn.cursor()
    cur.execute("INSERT INTO goals (goal, deadline) VALUES (%s, %s)", (goal, deadline))
    conn.commit()
    cur.close()

def show_goals(conn):
    cur = conn.cursor()
    cur.execute("SELECT goal, deadline FROM goals")
    rows = cur.fetchall()
    today = datetime.today().date()
    print("\n--- Your Goals ---")
    for row in rows:
        days_left = (row[1] - today).days
        print(f"Goal: {row[0]} | Days left: {days_left}")
    cur.close()

conn = connect()
setup(conn)
print("1. Add a goal")
print("2. View all goals")
choice = input("Choose: ")
if choice == "1":
    goal = input("Enter your goal: ")
    deadline = input("Enter deadline (YYYY-MM-DD): ")
    add_goal(conn, goal, deadline)
    print("Goal saved!")
elif choice == "2":
    show_goals(conn)
conn.close()
