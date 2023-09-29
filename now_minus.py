import pymysql
from datetime import datetime, timedelta

now= datetime.now()
print(f'now= {now}')

# Define a timedelta representing 300 days
delta = timedelta(days=300)

# Subtract 300 days from the current date and time
result_datetime = now - delta

print(result_datetime)
