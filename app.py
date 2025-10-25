from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pandas as pd
import model
import analysis
import utils

app = Flask(__name__)
model.init_db()

@app.route('/')
def home():
    expenses = model.fetch_expenses()
    df = model.fetch_expenses_df()
    categories_sums = model.fetch_category_sums()
    categories = [c[0] for c in categories_sums]
    amounts = [c[1] for c in categories_sums]
    pie_chart = utils.generate_pie_chart(categories, amounts)
    insights_data = analysis.generate_insights()
    insights = insights_data['insights']
    monthly_chart = insights_data['monthly_chart']
    forecast = insights_data['forecast']
    return render_template(
        'index.html',
        expenses=expenses,
        pie_chart=pie_chart,
        monthly_chart=monthly_chart,
        insights=insights,
        forecast=forecast
    )

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form.get('category')
    amount = float(request.form.get('amount', 0))
    note = request.form.get('note', '')
    model.insert_expense(category, amount, note)
    return redirect(url_for('home'))

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    model.delete_expense(expense_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
