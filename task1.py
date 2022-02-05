from connect import connect_db

with connect_db("C:/Users/gabbe/Downloads/Data Internship Task/data.sqlite") as conn:
 # exc = conn.execute("SELECT subscription_monthly_price, start_date, end_date from task WHERE strftime('%d',start_date) - strftime('%d',end_date) > 3;")

    # since there are no records with more than three days between end_date and start_date in terms of day of the month, it is reasonable to assume that all customers have paid for the months they have been subscribed

    # for i in exc.fetchmany(10):
    # print(i)

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
         SELECT 'total revenue in 2020: ' || CAST(SUM(revenue_2020) AS INT) || ' $', 'total revenue in 2021: ' || CAST(SUM(revenue_2021) AS INT) || ' $' \
        FROM cte_table")

    for i in exc2.fetchmany(10):
        print(i)

    conn.commit()
