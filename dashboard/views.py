from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Min, Max
from django.utils.timezone import now
from record.models import AddRecord
from .utlis import filter_records_by_period


# Create your views here.
@login_required
def dashboard_view(request):
    user = request.user   
    # 1️⃣ READ FILTER FROM GET (NOT POST)
    time_period = request.GET.get("time_period", "this_month")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # 2️⃣ BASE QUERYSET
    records = AddRecord.objects.filter(user=user)

    # 3️⃣ APPLY TIME FILTER
    filtered_records = filter_records_by_period(
        records, time_period, start_date, end_date
    ).order_by("-date")

    # 4️⃣ SUMMARY CARDS (FILTERED)
    total_income = (
        filtered_records.filter(type="Income")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_expenses = (
        filtered_records.filter(type="Expense")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_balance = total_income - total_expenses

    # 5️⃣ AVG DAILY EXPENSE (FILTERED RANGE)
    date_range = filtered_records.aggregate(
        first_date=Min("date"),
        last_date=Max("date")
    )

    if date_range["first_date"] and date_range["last_date"]:
        total_days = (date_range["last_date"] - date_range["first_date"]).days + 1
        avg_daily_expense = total_expenses / total_days if total_days > 0 else 0
    else:
        avg_daily_expense = 0

    # 6️⃣ CATEGORY CHART (FILTERED)
    category_data = (
        filtered_records
        .filter(type="Expense")
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    category_labels = [item["category"] for item in category_data]
    category_values = [float(item["total"]) for item in category_data]

    # 7️⃣ RECENT TRANSACTIONS (FILTERED, DATE-BASED)
    recent_5_records = filtered_records[:5]

    context = {
        "recent_5_records": recent_5_records,
        "total_balance": total_balance,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "avg_daily_expense": avg_daily_expense,
        "time_period": time_period,
        "category_labels": category_labels,
        "category_values": category_values,
    }

    return render(request, "dashboard/dashboard.html", context)
