from datetime import datetime

current_datetime = datetime.now()

new_datetime = current_datetime.replace(microsecond=0)

print("Original datetime:", current_datetime)
print("Datetime without microseconds:", new_datetime)