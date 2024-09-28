from datetime import datetime

# Your input string
input_string = '28/9/2024 15:00'

# Define the format of the input string
date_format = '%d/%m/%Y %H:%M'

# Parse the string into a datetime object
datetime_obj = datetime.strptime(input_string, date_format)

# Extract the date and time separately
date_part = datetime_obj.date()
time_part = datetime_obj.time()

print("Date:", date_part)
print("Time:", time_part)