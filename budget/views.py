from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AddBudget
from record.models import AddRecord
from dashboard.utlis import filter_records_by_period
from django.db.models import Sum

# --------------------------
# LIST ALL USER BUDGETS
# --------------------------
@login_required
def budget_list(request):
    user = request.user
    budgets = AddBudget.objects.filter(user=user)

    budget_data = []
    for b in budgets:
        spent = b.spent_amount()
        remaining = b.remaining()
        used_percent = b.used_percent()

        # dynamic color for UI
        if used_percent < 50:
            color = "#38b000"  # green
        elif used_percent < 80:
            color = "#ffb703"  # orange
        else:
            color = "#e63946"  # red

        budget_data.append({
            'id': b.id,
            'name': b.name,
            'amount': float(b.amount),
            'spent': spent,
            'remaining': remaining,
            'used_percent': round(used_percent, 2),
            'start_date': b.start_date,
            'end_date': b.end_date,
            'color': color,
        })

    return render(request, 'budget/budget_list.html', {'budgets': budget_data})




# --------------------------
# CREATE NEW BUDGET
# --------------------------
@login_required
def set_budget(request):
    if request.method == "POST":
        AddBudget.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            amount=request.POST.get('amount'),
        )
        return redirect('budget_list')
    return render(request, 'budget/set_budget.html')


# --------------------------
# EDIT EXISTING BUDGET
# --------------------------
@login_required
def edit_budget(request, budget_id):
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)
    
    if request.method == "POST":
        budget.name = request.POST.get('name')
        budget.start_date = request.POST.get('start_date')
        budget.end_date = request.POST.get('end_date')
        budget.amount = request.POST.get('amount')
        budget.save()
        return redirect('budget_list')

    return render(request, 'budget/edit_budget.html', {'budget': budget})


# --------------------------
# RESET BUDGET (DELETE ITS TRANSACTIONS)
# --------------------------
@login_required
def delete_budget(request, budget_id):
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)
    if request.method == "POST":
        AddRecord.objects.filter(user=user, budget=budget).delete()  # delete all linked records
        budget.delete()
        return redirect('budget_list')

    return render(request, 'budget/delete_budget.html', {'budget': budget})

@login_required
def add_expense_with_budget(request, budget_id):
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)

    if request.method == 'POST':
        date_ = request.POST.get('date')
        type_ = request.POST.get('type')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        amount = request.POST.get('amount')

        # Add record if record fields are present
        if date_ and type_ and category and amount:
            AddRecord.objects.create(
                user=user,
                budget=budget,
                date=date_,
                type=type_,
                category=category,
                description=description,
                amount=float(amount)
            )    
            return redirect('budget_list')
    
    return render(request, 'budget/add_expense_with_budget.html', {'budget_name': budget.name})

@login_required
def view_expense_with_budget(request, budget_id):
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)

    expense_list = AddRecord.objects.filter(
        user=user,
        budget=budget,
        type='Expense',
        ).order_by('-created_at')
    
    context ={
        'budget':budget,
        'expense_list':expense_list,
    }

    return render(request, 'budget/view_expense_with_budget.html', context)
