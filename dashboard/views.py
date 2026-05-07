from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Min, Max
from django.utils.timezone import now
from record.models import AddRecord
from .utlis import filter_records_by_period
from budget.models import AddBudget

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
    total_income = records.filter(type="Income").aggregate(total_income=Sum("amount"))["total_income"] or 0
    total_expense = records.filter(type="Expense").aggregate(total_expense=Sum("amount"))["total_expense"] or 0
    total_balance = total_income - total_expense
    total_active_budgets = AddBudget.objects.filter(user=user, status="active").count()
   


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
        "total_expenses": total_expense,
        "total_active_budgets": total_active_budgets,
        "time_period": time_period,
        "category_labels": category_labels,
        "category_values": category_values,
    }
    

    return render(request, "dashboard/dashboard.html", context)


