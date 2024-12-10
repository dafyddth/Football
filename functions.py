from datetime import datetime


def time_from_string(date_time_string):
    date_formats = ['%d/%m/%Y %H:%M', '%d/%m/%Y']
    for date_format in date_formats:
        try:
            datetime_obj = datetime.strptime(date_time_string, date_format)
            return datetime_obj.time()
        except ValueError:
            continue
    # If no time part is found, return 00:00
    return time(0, 0)


def date_from_string(date_time_string):
    date_formats = ['%d/%m/%Y %H:%M', '%d/%m/%Y']
    for date_format in date_formats:
        try:
            datetime_obj = datetime.strptime(date_time_string, date_format)
            return datetime_obj.date()
        except ValueError:
            continue
    raise ValueError("Date string does not match any expected format")


def percentage_to_decimal_odds(percentage):
    # Convert the percentage to a decimal
    probability = percentage / 100.0
    # Calculate the decimal odds
    decimal_odds = round(1 / probability, 1)
    return decimal_odds



def return_one():
    return 1

