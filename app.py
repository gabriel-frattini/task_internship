import plotly.express as px
import sqlite3
import pandas as pd
import datetime as dt
import streamlit

connection = sqlite3.connect("data.sqlite")

lists = []
with connection as conn:
    exc = conn.execute(
        "SELECT subscription_monthly_price, start_date,end_date FROM task")
    for i in exc.fetchall():
        lists.append(i)

df = pd.DataFrame(
    lists, columns=["monthly_price", "start", "end"]).reset_index()

new_dates = []
df2 = pd.DataFrame()
lists = []

for index, i in enumerate(df.start):
    y = i.split("-")
    start_month = int(y[1])
    end_d = df.end[index].split('-')
    diff = pd.to_datetime(i) - pd.to_datetime(df.end[index])
    month_diff = abs(int(diff.days/31))

    for month in range(month_diff+1):
        if month+start_month < 10:
            date = f'{y[0]}-0{month+start_month}'
        else:
            date = f'{y[0]}-{month+start_month}'

        if month+start_month > 12:
            date = f'2021-{(month+start_month)-12}'
            new_dates.append([date, index])
        else:
            new_dates.append([date, index])

df_dates = pd.DataFrame(new_dates, columns=["date", "index"])

df_all = df.merge(df_dates, left_on=df["index"], right_on=df_dates["index"])
df_all = df_all.drop(["key_0", "index_y"], axis=1)
df_all["monthly_price"] = pd.to_numeric(df_all.monthly_price)

price_months = df_all.groupby("date")["monthly_price"].sum()
price_months = price_months.reset_index()

price_months["date"] = pd.to_datetime(price_months.date)
price_months["month"] = price_months.date.dt.strftime('%b')
years = [str(i.year) for i in price_months.date]

price_months = pd.concat([price_months, pd.Series(years, name="year")], axis=1)

plot_task1 = px.line(price_months, x="month", y="monthly_price", color="year",
        title="Revenue Generated for 2020 & 2021")


monthly_subscriptions = []
with connection as conn:
    exc = conn.execute(
        "SELECT CAST(SUM(subscription_monthly_price) AS INT) AS total, strftime('%Y-%m',start_date) AS month FROM task GROUP BY month ORDER BY total DESC")
    for i in exc.fetchall():
        monthly_subscriptions.append(i)

y = pd.DataFrame(lists, columns=["revenue", "date"])
y["date"] = pd.to_datetime(y.date)
y["revenue"] = pd.to_numeric(y.revenue)

y = y.sort_values("date")
px.line(y, x="date", y="revenue",
        title="Revenue $ Generated from new subscriptions")



monthly_subscriptions = []
with connection as conn:
    exc = conn.execute(
        "SELECT CAST(SUM(subscription_monthly_price) AS INT) AS total, strftime('%Y-%m',start_date) AS month FROM task GROUP BY month ORDER BY total DESC")
    for i in exc.fetchall():
        monthly_subscriptions.append(i)

df_revenue = pd.DataFrame(monthly_subscriptions, columns=["revenue", "date"])
df_revenue["date"] = pd.to_datetime(df_revenue.date)
df_revenue["revenue"] = pd.to_numeric(df_revenue.revenue)

df_revenue = df_revenue.sort_values("date")
plot_task2 = px.line(df_revenue, x="date", y="revenue",
        title="Revenue $ Generated from new subscriptions")

streamlit.plotly_chart(plot_task1)
streamlit.plotly_chart(plot_task2)
