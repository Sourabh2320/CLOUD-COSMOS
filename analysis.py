import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, List, Dict
from model import fetch_expenses_df, fetch_category_sums
from utils import generate_monthly_bar

def _safe_float(x):
    try:
        return float(x)
    except:
        return 0.0

def monthly_summary(df: pd.DataFrame) -> Dict[str, float]:
    if df.empty:
        return {"total": 0.0, "average": 0.0, "months_recorded": 0}
    df['amount'] = df['amount'].apply(_safe_float)
    total = df['amount'].sum()
    average = df['amount'].mean()
    months = pd.to_datetime(df['date']).dt.to_period('M').nunique()
    return {"total": float(total), "average": float(average), "months_recorded": int(months)}

def top_category(df: pd.DataFrame) -> Tuple[str, float]:
    if df.empty:
        return ("None", 0.0)
    s = df.groupby('category')['amount'].sum()
    if s.empty:
        return ("None", 0.0)
    top = s.idxmax()
    val = float(s.max())
    return (top, val)

def month_series(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=float)
    df['date'] = pd.to_datetime(df['date'])
    series = df.set_index('date').resample('M')['amount'].sum()
    series.index = series.index.to_period('M').to_timestamp()
    return series

def forecast_next_month(df: pd.DataFrame) -> float:
    series = month_series(df)
    if series.empty or len(series) < 2:
        return float(series.iloc[-1]) if len(series) == 1 else 0.0
    y = series.values
    x = np.arange(len(y))
    coef = np.polyfit(x, y, 1)
    pred = coef[0] * (len(y)) + coef[1]
    if pred < 0:
        pred = float(max(y.mean(), 0.0))
    return float(pred)

def trend_analysis(df: pd.DataFrame) -> str:
    series = month_series(df)
    if series.empty or len(series) < 2:
        return "Not enough data to determine trend."
    y = series.values
    x = np.arange(len(y))
    m = np.polyfit(x, y, 1)[0]
    if m > 0:
        return "Your monthly spending is trending upward."
    if m < 0:
        return "Your monthly spending is trending downward."
    return "Your monthly spending is stable."

def savings_suggestion(total_monthly: float, top_cat_name: str, top_cat_amount: float) -> str:
    if total_monthly <= 0:
        return "No spending data yet to suggest savings."
    suggested_cut = min(top_cat_amount * 0.1, total_monthly * 0.15)
    suggestion = f"Try reducing {top_cat_name} by ₹{suggested_cut:.0f} per month to save more."
    return suggestion

def generate_insights() -> Dict:
    df = fetch_expenses_df()
    summary = monthly_summary(df)
    top_cat_name, top_cat_amount = top_category(df)
    forecast = forecast_next_month(df)
    trend = trend_analysis(df)
    monthly_chart = generate_monthly_bar(df)
    insights: List[str] = []
    if summary["total"] == 0:
        insights.append("No expenses recorded yet. Start adding expenses to get insights.")
    else:
        insights.append(f"Total spent: ₹{summary['total']:.2f}")
        insights.append(f"Average per transaction: ₹{summary['average']:.2f}")
        insights.append(f"Top category: {top_cat_name} (₹{top_cat_amount:.2f})")
        insights.append(trend)
        insights.append(f"Predicted next month spending: ₹{forecast:.2f}")
        insights.append(savings_suggestion(summary["total"], top_cat_name, top_cat_amount))
        if summary["total"] > 5000:
            insights.append("You are spending over ₹5000 — consider stricter limits or budgets.")
        elif summary["total"] < 2000 and summary["total"] > 0:
            insights.append("Good job! Your spending is under control this month.")
    return {"insights": insights, "monthly_chart": monthly_chart, "forecast": float(forecast)}
