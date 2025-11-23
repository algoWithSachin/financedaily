from datetime import date, timedelta

def filter_records_by_period(record_list, time_period, start_date=None, end_date=None):

    today = date.today()
    if time_period == "today":
        record_list = record_list.filter(date=today)

    elif time_period == "this_week":
        start_week = today - timedelta(days=today.weekday())
        record_list = record_list.filter(date__range=[start_week, today])

    elif time_period == "this_month":
        record_list = record_list.filter(date__year=today.year, date__month=today.month)

    elif time_period == "this_year":
        record_list = record_list.filter(date__year=today.year)

    elif time_period == "custom":
         record_list = record_list.filter(date__range=[start_date, end_date])  

    else:
        return record_list  # if user select all records

    return record_list  