from datetime import datetime

date_1 = input("Enter Date 1 (YYYY-MM-DD HH:MM:SS): ")
date_2 = input("Enter Date 2 (YYYY-MM-DD HH:MM:SS): ")

d_1 = datetime.strptime(date_1, "%Y-%m-%d %H:%M:%S")
d_2 = datetime.strptime(date_2, "%Y-%m-%d %H:%M:%S")

difference = d_1 - d_2

seconds = abs(difference.total_seconds())   

print("Difference in seconds:", seconds)

# 2025-10-05 12:00:00
# 2025-10-03 08:30:00