
from datetime import date, timedelta
import calendar
from django.db.models import Sum

# ─────────────────────────────────────────
# HELPER: Filter records by time period
# ─────────────────────────────────────────
def filter_records_by_period(queryset, period, start_date=None, end_date=None):
    """
    Filter a queryset of records by time period.
    Supports: this_month, last_month, this_week, last_week, 
              last_7_days, last_30_days, this_year, custom
    """
    today = date.today()
    
    if period == "this_month":
        return queryset.filter(
            date__year=today.year,
            date__month=today.month
        )
    
    elif period == "last_month":
        # Handle January → December wrap
        if today.month == 1:
            return queryset.filter(date__year=today.year - 1, date__month=12)
        else:
            return queryset.filter(date__year=today.year, date__month=today.month - 1)
    
    elif period == "this_week":
        # Week starts on Monday (isocalendar)
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        return queryset.filter(date__range=[week_start, week_end])
    
    elif period == "last_week":
        week_start = today - timedelta(days=today.weekday() + 7)
        week_end = week_start + timedelta(days=6)
        return queryset.filter(date__range=[week_start, week_end])
    
    elif period == "last_7_days":
        return queryset.filter(date__gte=today - timedelta(days=7))
    
    elif period == "last_30_days":
        return queryset.filter(date__gte=today - timedelta(days=30))
    
    elif period == "this_year":
        return queryset.filter(date__year=today.year)
    
    elif period == "custom" and start_date and end_date:
        return queryset.filter(date__range=[start_date, end_date])
    
    # Default: this month
    return queryset.filter(date__year=today.year, date__month=today.month)

    


# ─────────────────────────────────────────
# HELPER: Get trend data for charts
# ─────────────────────────────────────────
def get_trend_data(records, period):
    """
    Generate daily/weekly trend data for Income vs Expense chart.
    Returns labels, income_values, expense_values.
    """
    today = date.today()
    
    if period in ["last_7_days", "this_week", "last_week"]:
        # Daily breakdown for short periods
        days = 7 if period in ["this_week", "last_week"] else 7
        if period == "this_week":
            start = today - timedelta(days=today.weekday())
        elif period == "last_week":
            start = today - timedelta(days=today.weekday() + 7)
        else:
            start = today - timedelta(days=6)
        
        labels = []
        income_data = []
        expense_data = []
        
        for i in range(days):
            current = start + timedelta(days=i)
            labels.append(current.strftime("%a %d"))  # e.g., "Mon 15"
            
            day_records = records.filter(date=current)
            income_data.append(
                float(day_records.filter(type__iexact="Income").aggregate(total=Sum("amount"))["total"] or 0)
            )
            expense_data.append(
                float(day_records.filter(type__iexact="Expense").aggregate(total=Sum("amount"))["total"] or 0)
            )
        
        return labels, income_data, expense_data
    
    elif period in ["this_month", "last_month", "last_30_days"]:
        # Weekly breakdown for monthly periods
        if period == "last_month":
            if today.month == 1:
                year, month = today.year - 1, 12
            else:
                year, month = today.year, today.month - 1
            _, last_day = calendar.monthrange(year, month)
            start = date(year, month, 1)
            end = date(year, month, last_day)
        elif period == "last_30_days":
            start = today - timedelta(days=29)
            end = today
        else:
            _, last_day = calendar.monthrange(today.year, today.month)
            start = date(today.year, today.month, 1)
            end = date(today.year, today.month, last_day)
        
        labels = []
        income_data = []
        expense_data = []
        
        # Split into 4 weeks
        week_starts = [start + timedelta(days=i*7) for i in range(4)]
        
        for i, week_start in enumerate(week_starts):
            week_end = min(week_start + timedelta(days=6), end)
            labels.append(f"Week {i+1}")
            
            week_records = records.filter(date__range=[week_start, week_end])
            income_data.append(
                float(week_records.filter(type__iexact="Income").aggregate(total=Sum("amount"))["total"] or 0)
            )
            expense_data.append(
                float(week_records.filter(type__iexact="Expense").aggregate(total=Sum("amount"))["total"] or 0)
            )
        
        return labels, income_data, expense_data
    
    elif period == "this_year":
        # Monthly breakdown for yearly
        labels = []
        income_data = []
        expense_data = []
        
        for month in range(1, 13):
            labels.append(calendar.month_abbr[month])  # "Jan", "Feb", etc.
            month_records = records.filter(date__year=today.year, date__month=month)
            income_data.append(
                float(month_records.filter(type__iexact="Income").aggregate(total=Sum("amount"))["total"] or 0)
            )
            expense_data.append(
                float(month_records.filter(type__iexact="Expense").aggregate(total=Sum("amount"))["total"] or 0)
            )
        
        return labels, income_data, expense_data
    
    elif period == "custom":
        # For custom range, show daily if <= 31 days, weekly if > 31 days
        # This is a simplified version - assumes start_date and end_date are available
        labels = ["Period Total"]
        income_data = [
            float(records.filter(type__iexact="Income").aggregate(total=Sum("amount"))["total"] or 0)
        ]
        expense_data = [
            float(records.filter(type__iexact="Expense").aggregate(total=Sum("amount"))["total"] or 0)
        ]
        return labels, income_data, expense_data
    
    # Default fallback
    return ["No Data"], [0], [0]


