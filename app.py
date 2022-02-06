import plotly.express as px
import sqlite3
import pandas as pd
import datetime as dt
import streamlit as st

connection = sqlite3.connect("data.sqlite")

    # connecting to sqllite and appending data to list
lists = []
with connection as conn:
    exc = conn.execute(
        "SELECT subscription_monthly_price, start_date,end_date FROM task")
    for i in exc.fetchall():
        lists.append(i)

        # making it in to a dataframe
df = pd.DataFrame(
    lists, columns=["monthly_price", "start", "end"]).reset_index()

# creating a df for all months with subscriptions
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

# merging and grouping df with revenue and dates

df_all = df.merge(df_dates, left_on=df["index"], right_on=df_dates["index"])
df_all = df_all.drop(["key_0", "index_y"], axis=1)
df_all["monthly_price"] = pd.to_numeric(df_all.monthly_price)

price_months = df_all.groupby("date")["monthly_price"].sum()
price_months = price_months.reset_index()

price_months["date"] = pd.to_datetime(price_months.date)
price_months["month"] = price_months.date.dt.strftime('%b')
years = [str(i.year) for i in price_months.date]

price_months = pd.concat([price_months, pd.Series(years, name="year")], axis=1)

#plot for task 1

plot_task1 = px.line(price_months.sort_values("date"), x="month", y="monthly_price", color="year",
        title="Revenue Generated for 2020 & 2021")

# sql query for task 2

monthly_subscriptions = []
with connection as conn:
    exc = conn.execute(
        "SELECT CAST(SUM(subscription_monthly_price) AS INT) AS total, strftime('%Y-%m',start_date) AS month FROM task GROUP BY month ORDER BY total DESC")
    for i in exc.fetchall():
        monthly_subscriptions.append(i)

    # queries for task 2
 
monthly_subscriptions = []
with connection as conn:
    exc = conn.execute(
        "SELECT CAST(SUM(subscription_monthly_price) AS INT) AS total, strftime('%Y-%m',start_date) AS month FROM task GROUP BY month ORDER BY total DESC")
    for i in exc.fetchall():
        monthly_subscriptions.append(i)

        #adding monthly revenue and date to df
        
df_revenue = pd.DataFrame(monthly_subscriptions, columns=["revenue", "date"])
df_revenue["date"] = pd.to_datetime(df_revenue.date)
df_revenue["revenue"] = pd.to_numeric(df_revenue.revenue)

df_revenue = df_revenue.sort_values("date")
plot_task2 = px.line(df_revenue, x="date", y="revenue",
        title="Revenue $ Generated from new subscriptions")


    # streamlit wepage

st.title("Task submission for internship at CARIFY")

st.header("1.")
st.subheader("What was the total revenues generated in the year 2020 and 2021, respectively?")

st.plotly_chart(plot_task1)

with connection as conn:
    exc2 = conn.execute("WITH RECURSIVE cte_table(revenue_2020, revenue_2021) AS (\
        SELECT CASE \
        WHEN strftime('%Y',end_date)=='2021' AND strftime('%Y',start_date)=='2020' \
            THEN ((JULIANDAY('2021-01-' || strftime('%d',start_date)) - JULIANDAY(start_date))/30) * subscription_monthly_price \
        ELSE ((JULIANDAY(end_date) - JULIANDAY(start_date))/30) * subscription_monthly_price\
            END revenue_2020, \
        CASE WHEN strftime('%Y',end_date)=='2021' AND strftime('%Y',start_date)=='2020' \
            THEN ((JULIANDAY(end_date) - (JULIANDAY('2021-01-' || strftime('%d',start_date))))/30) * subscription_monthly_price END revenue_2021\
         FROM task)\
         \
         SELECT CAST(SUM(revenue_2020) AS INT) || ' $', CAST(SUM(revenue_2021) AS INT) || ' $' \
        FROM cte_table")

    for i in exc2.fetchall():
        revenue_20 = i[0]
        revenue_21 = i[1]

col1, col2 = st.columns(2)

with col1:
    click_20 = st.button("Revenue generated for 2020")
    if click_20:
    st.subheader(revenue_20)

with col2:
    click_21 = st.button("Revenue generated for 2021")
    if click_21:
    st.subheader(revenue_21)
    

with connection as conn:

    exc2 = conn.execute(
        "SELECT CAST(SUM(subscription_monthly_price) AS INT) AS total, strftime('%Y-%m',start_date) AS month FROM task GROUP BY month ORDER BY total DESC LIMIT 1")

    fetch = exc2.fetchone()

st.header("2.")
st.subheader("Identify the month with the highest amount of revenues arising from new subscriptions")

st.plotly_chart(plot_task2)
button = st.button("Month with the highest amount of revenue arising from new subscriptions")

if button:
    st.subheader( f'The date was {fetch[1]} and a total of {fetch[0]} $ was generated from this month')
