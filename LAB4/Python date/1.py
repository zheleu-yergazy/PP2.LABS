from datetime import date, timedelta

date_now = date.today()

new_date = date_now - timedelta(5)

print(date_now)
print(new_date)