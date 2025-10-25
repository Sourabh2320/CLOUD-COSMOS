import sqlite3
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd

def get_db_connection():
    conn = sqlite3.connect('database/trackify.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_pie_chart(categories, amounts):
    if not categories or not amounts:
        return None
    plt.switch_backend('Agg')
    plt.figure(figsize=(5, 5))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Breakdown by Category')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return chart_url

def generate_monthly_bar(df: pd.DataFrame):
    if df.empty:
        return None
    df['date'] = pd.to_datetime(df['date'])
    monthly = df.set_index('date').resample('M')['amount'].sum()
    plt.switch_backend('Agg')
    plt.figure(figsize=(6, 4))
    monthly.plot(kind='bar', color='skyblue')
    plt.title('Month-wise Spending Trend')
    plt.ylabel('Amount (₹)')
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url
