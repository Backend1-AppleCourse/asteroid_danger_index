from datetime import datetime, timedelta

def generate_date_ranges(month, year):
    # Calculate the number of days in the month
    if month == 12:
        next_month_first_day = datetime(year + 1, 1, 1)
    else:
        next_month_first_day = datetime(year, month + 1, 1)
    
    last_day_of_month = next_month_first_day - timedelta(days=1)
    start_date = datetime(year, month, 1)
    
    date_ranges = []
    
    while start_date <= last_day_of_month:
        end_date = start_date + timedelta(days=6)
        # Ensure the end_date does not exceed the last day of the month
        if end_date > last_day_of_month:
            end_date = last_day_of_month
        
        date_ranges.append((start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        # Set the next start_date as the day after the current end_date
        start_date = end_date + timedelta(days=1)
    
    return date_ranges