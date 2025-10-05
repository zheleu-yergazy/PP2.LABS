from datetime import date, timedelta

date_now = date.today()
date_yesterday = date_now - timedelta(1)
date_tomorrow = date_now + timedelta(1)

print(f"today: {date_now}")
print(f"yesterday: {date_yesterday}")
print(f"tomorrow: {date_tomorrow}")
