import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = 'database/trackify.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount REAL,
        date TEXT,
        note TEXT
    )''')
    conn.commit()
    conn.close()

def insert_expense(category: str, amount: float, note: str):
    conn = sqlite3.connect(DB_PATH)
    date = datetime.now().strftime("%Y-%m-%d")
    conn.execute("INSERT INTO expenses (category, amount, date, note) VALUES (?, ?, ?, ?)",
                 (category, amount, date, note))
    conn.commit()
    conn.close()

def delete_expense(expense_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def fetch_expenses() -> list:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    data = cur.fetchall()
    conn.close()
    return data

def fetch_expenses_df() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df

def fetch_category_sums() -> list:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cur.fetchall()
    conn.close()
    return data
