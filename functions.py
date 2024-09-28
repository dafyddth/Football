from datetime import datetime


def time_from_string(date_time_string):
    date_format = '%d/%m/%Y %H:%M'
    datetime_obj = datetime.strptime(date_time_string, date_format)
    time_part = datetime_obj.time()
    return time_part


def date_from_string(date_time_string):
    date_format = '%d/%m/%Y %H:%M'
    datetime_obj = datetime.strptime(date_time_string, date_format)
    date_part = datetime_obj.date()
    return date_part


def percentage_to_decimal_odds(percentage):
    # Convert the percentage to a decimal
    probability = percentage / 100.0
    # Calculate the decimal odds
    decimal_odds = round(1 / probability, 1)
    return decimal_odds
