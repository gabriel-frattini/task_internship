from connect import connect_db

with connect_db("data.sqlite") as conn:

    exc2 = conn.execute(
        "SELECT CAST(SUM(subscription_monthly_price) AS INT) AS total, strftime('%Y-%m',start_date) AS month FROM task GROUP BY month ORDER BY total DESC LIMIT 1")

    fetch = exc2.fetchone()

    print(
        f'The month with the highest amount of revenues generated from new subscriptions was in {fetch[1]} and was a total of {fetch[0]} $')
