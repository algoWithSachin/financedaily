from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from record.models import AddRecord
from django.db.models import Sum, Max, Min
from .utlis import filter_records_by_period

# Create your views here.
@login_required
def dashboard_view(request):
    user = request.user

    # Retrieve all records belonging to logged-in user
    recent_record = AddRecord.objects.filter(user=user)

    if 'time_period' in request.POST:
        time_period = request.POST.get("time_period")
    else:
        time_period = "all_records"

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    # Filter records with selected time period
    filter_record = filter_records_by_period(recent_record, time_period, start_date, end_date)
    filter_record = filter_record.order_by('-date')

    # Cards values
    total_income = filter_record.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = filter_record.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0

    # find first and last record dates
    record_dates = AddRecord.objects.filter(user=user).aggregate(
        first_date=Min('date'),
        last_date=Max('date')
    )
    if record_dates['first_date'] and record_dates['last_date']:
        total_days = (record_dates['last_date'] - record_dates['first_date']).days + 1
        avg_daily_expense = total_expenses / total_days if total_days > 0 else 0
    else:
        avg_daily_expense = 0

    total_balance = total_income - total_expenses

    # Category breakdown for chart
    category_data = (
        filter_record
        .filter(type='Expense')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    category_labels = [item['category'] for item in category_data]
    category_values = [float(item['total']) for item in category_data]

    # Recent records
    recent_5_records = recent_record.order_by('-created_at')[:5]

    context = {
        'recent_5_records': recent_5_records,
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'avg_daily_expense': avg_daily_expense,
        'time_period': time_period,
        'category_labels': category_labels,
        'category_values': category_values,
    }

    return render(request, 'dashboard/dashboard.html', context)
