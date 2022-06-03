from datetime import datetime


i_timestamp = 1654032566
f_timestamp = 1654032577
price = 200
total_seconds = f_timestamp - i_timestamp
total_hours = total_seconds/3600

total_hours = round(total_hours)

print(datetime.fromtimestamp(i_timestamp))
print(datetime.fromtimestamp(f_timestamp))
