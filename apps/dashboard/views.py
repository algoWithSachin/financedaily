
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from datetime import date
import json
import calendar

from apps.record.models import AddRecord
from apps.budget.models import AddBudget

from .utlis import filter_records_by_period, get_trend_data




# ─────────────────────────────────────────
# MAIN DASHBOARD VIEW
# ─────────────────────────────────────────
@login_required
def dashboard_view(request):
    user = request.user
    today = date.today() 
    # 1️⃣ READ FILTER FROM GET
    time_period = request.GET.get("period", "this_month")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    

    # 2️⃣ BASE QUERYSET (all user records)
    all_records = AddRecord.objects.filter(user=user)
    
    # 3️⃣ APPLY TIME FILTER
    filtered_records = filter_records_by_period(
        all_records, time_period, start_date, end_date
    ).order_by("-date")

    # ── SUMMARY CARDS (FILTERED) ──
    total_income = (
        filtered_records.filter(type__iexact="Income")
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    total_expense = (
        filtered_records.filter(type__iexact="Expense")
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    total_balance = total_income - total_expense
    
    total_active_budgets = AddBudget.objects.filter(
        user=user, status="active"
    ).count()

    # ── BUDGET CARDS (with auto-status update) ──
    active_budgets = AddBudget.objects.filter(user=user, status="active")
    # Auto-update expired budgets
    for budget in active_budgets:
        budget.auto_update_status()
    
    # Refresh after potential status changes
    active_budgets = AddBudget.objects.filter(user=user, status="active")

    # ── TREND CHART DATA ──
    trend_labels, trend_income, trend_expense = get_trend_data(
        filtered_records, time_period
    )

    # ── CATEGORY CHART (FILTERED) ──
    category_data = (
        filtered_records
        .filter(type__iexact="Expense")
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:8]  # Top 8 categories
    )

    category_labels = [item["category"] for item in category_data]
    category_values = [float(item["total"]) for item in category_data]

    # ── RECENT TRANSACTIONS (FILTERED) ──
    
    recent_5_records = filtered_records.order_by("date")[:5]

    # ── ADDITIONAL INSIGHTS ──
    # Highest expense category
    highest_expense_category = category_data.first() if category_data else None
    
    # Transaction count in period
    transaction_count = filtered_records.count()
    
    # Average daily spend (for monthly periods)
    avg_daily_spend = 0
    if time_period in ["this_month", "last_month"] and total_expense > 0:
        if time_period == "this_month":
            days_passed = today.day
            avg_daily_spend = total_expense / max(days_passed, 1)
        else:
            # Last month - use total days in that month
            if today.month == 1:
                _, days_in_month = calendar.monthrange(today.year - 1, 12)
            else:
                _, days_in_month = calendar.monthrange(today.year, today.month - 1)
            avg_daily_spend = total_expense / days_in_month

    # ── CONTEXT ──
    context = {
        # Core metrics
        "recent_5_records": recent_5_records,
        "total_balance": total_balance,
        "total_income": total_income,
        "total_expenses": total_expense,
        "total_active_budgets": total_active_budgets,
        
        # Filter state
        "time_period": time_period,
        "start_date": start_date,
        "end_date": end_date,
        "selected_period": time_period,
        
        # Chart data (JSON serialized)
        "category_labels": json.dumps(category_labels),
        "category_values": json.dumps(category_values),
        "trend_labels": json.dumps(trend_labels),
        "trend_income": json.dumps(trend_income),
        "trend_expense": json.dumps(trend_expense),
        
        # Budget cards
        "active_budgets": active_budgets,
        
        # Extra insights
        "transaction_count": transaction_count,
        "avg_daily_spend": round(avg_daily_spend, 2),
        "highest_expense_category": highest_expense_category["category"] if highest_expense_category else "None",
    }

    return render(request, "dashboard/new.html", context)



