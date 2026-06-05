from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AddRecord
from django.db.models import Sum
from apps.dashboard.utlis import filter_records_by_period
    
        


# ================================
# RECORD LIST / VIEW
# ================================
@login_required
def record_view(request):
    user = request.user
    record_list = AddRecord.objects.filter(user=user).order_by('-created_at')

    # Time period filter
    time_period = request.POST.get("time_period", "all_records")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    filtered_records = filter_records_by_period(record_list, time_period, start_date, end_date)

    # Aggregate for summary cards
    total_income = filtered_records.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = filtered_records.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_balance = total_income - total_expenses

    if total_income + total_expenses > 0:
        income_percent = (total_income / (total_income + total_expenses)) * 100
        expense_percent = 100 - income_percent
    else:
        income_percent = expense_percent = 0

    context = {
        'recent_records': filtered_records,
        "income_records": record_list.filter(type="Income"),
        "expense_records": record_list.filter(type="Expense"),
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'time_period': time_period,
        'income_percent': round(income_percent, 2),
        'expense_percent': round(expense_percent, 2),
    }
    return render(request, 'record/record.html', context)


# ================================
# ADD RECORD
# ================================
@login_required
def add_record(request):
    if request.method == 'POST':
        user = request.user
        date_ = request.POST.get('date')
        type_ = request.POST.get('type')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        amount = request.POST.get('amount')


        if date_ and type_ and category and amount:
            AddRecord.objects.create(
                user=user,
                date=date_,
                type=type_,
                category=category,
                description=description,
                amount=float(amount)
            )
            messages.success(request, "Record added successfully!")
            
            return redirect('record_list')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'record/add_record.html')


# ================================
# EDIT RECORD
# ================================
@login_required
def edit_record(request, record_id):
    record = get_object_or_404(AddRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        record.date = request.POST.get('date')
        record.type = request.POST.get('type')
        record.category = request.POST.get('category')
        record.description = request.POST.get('description')
        record.amount = request.POST.get('amount')
        record.save()
        messages.success(request, "Record updated successfully!")

        next_url = request.POST.get('next')
        return redirect(next_url or 'record_list')

    return render(request, 'record/edit_record.html', {'record': record})


# ================================
# DELETE RECORD
# ================================
@login_required
def delete_record(request, record_id):
    record = get_object_or_404(AddRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Record deleted successfully!")

        next_url = request.POST.get('next')

        return redirect(next_url or 'record_list')

    return render(request, 'record/delete_record.html', {'record': record})

