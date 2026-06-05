from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AddBudget
from .utlis import *
from django.db.models import Sum, Q

# ==========================
# LIST ALL USER BUDGETS
# ==========================
@login_required
def budget_list(request):
    user = request.user

    # Only active budgets, DB-level filter
    budgets = AddBudget.objects.filter(user=user, status="active")

    active_budgets = []

    for b in budgets:
        # Calculate spent, remaining, used % once
        spent = b.spent_amount()
        remaining = float(b.amount) - spent
        used_percent = (spent / float(b.amount)) * 100 if b.amount else 0

        # Color logic
        if used_percent < 50:
            color = "#38b000"
        elif used_percent < 80:
            color = "#ffb703"
        else:
            color = "#e63946"

        active_budgets.append({
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

    return render(request, 'budget/budget_list.html', {'budgets': active_budgets})


# ==========================
# CREATE NEW BUDGET
# ==========================

@login_required
def set_budget(request):
    from datetime import date
    if request.method == "POST":
        name = request.POST.get('name', 'Budget')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        amount_str = request.POST.get('amount')

        # Convert strings to proper types
        try:
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('set_budget')

        try:
            amount = float(amount_str)
        except ValueError:
            messages.error(request, "Amount must be a number.")
            return redirect('set_budget')

        # Validate dates and amount
        if not validate_budget_dates(request, start_date, end_date, name):
            return redirect('set_budget')

        if not validate_budget_amount(request, amount, name):
            return redirect('set_budget')

        # Everything valid → create budget
        AddBudget.objects.create(
            user=request.user,
            name=name,
            start_date=start_date,
            end_date=end_date,
            amount=amount,
        )
        messages.success(request, f"Budget '{name}' created successfully!")
        return redirect('budget_list')

    return render(request, 'budget/set_budget.html')


# ==========================
# EDIT EXISTING BUDGET
# ==========================
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
        messages.success(request, "Budget updated successfully!")
        return redirect('budget_list')

    return render(request, 'budget/edit_budget.html', {'budget': budget})

# ==========================
# DELETE BUDGET (RESET)
# ==========================
@login_required
def delete_budget(request, budget_id):
    from apps.record.models import AddRecord
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)
    if request.method == "POST":
        AddRecord.objects.filter(user=user, budget=budget).delete()  # delete all linked records
        budget.delete()
        messages.success(request, "Budget and its transactions deleted successfully!")
        return redirect('budget_list')

    return render(request, 'budget/delete_budget.html', {'budget': budget})

# ==========================
# ADD EXPENSE TO SPECIFIC BUDGET
# ==========================
@login_required
def add_expense_with_budget(request, budget_id):
    from apps.record.models import AddRecord
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)

    if request.method == 'POST':
        date_ = request.POST.get('date')
        type_ = request.POST.get('type', 'Expense')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        amount = request.POST.get('amount')

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
            messages.success(request, f"Expense added to '{budget.name}' successfully!")
            return redirect('budget_list')
        else:
            messages.error(request, "All fields are required to add an expense.")

    # Pass the whole budget object to the template
    return render(request, 'budget/add_expense_with_budget.html', {'budget': budget, 'budget_name': budget.name})

# ==========================
# VIEW EXPENSES LINKED TO BUDGET
# ==========================
@login_required
def view_expense_with_budget(request, budget_id):
    from apps.record.models import AddRecord
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)

    expense_list = AddRecord.objects.filter(
        user=user,
        budget=budget,
        type='Expense',
    ).order_by('-created_at')
    
    context = {
        'budget': budget,
        'expense_list': expense_list,
    }

    return render(request, 'budget/view_expense_with_budget.html', context)

@login_required
def view_completed_budget_expenses(request, budget_id):
    from apps.record.models import AddRecord
    user = request.user
    budget = get_object_or_404(AddBudget, id=budget_id, user=user)

    if budget.status != 'completed':
        messages.error(request, "Budget is not completed.")
        return redirect('budget_list')

    expense_list = AddRecord.objects.filter(user=user, budget=budget)

    return render(request, 'budget/view_completed_budget_expenses.html', {
        'budget': budget,
        'expense_list': expense_list,
    })

# ==========================
# BUDGET COMPLETED
# ==========================
@login_required
def budget_completed_view(request):
    user = request.user
    budgets = AddBudget.objects.filter(user=user)
    completed_list = []

    for b in budgets:
        b.auto_update_status()  # Only here we need update

        if b.status != "completed":
            continue

        spent = b.spent_amount()
        remaining = float(b.amount) - spent
        used_percent = (spent / float(b.amount)) * 100 if b.amount else 0

        badge = "under" if used_percent < 100 else "normal" if used_percent == 100 else "over"

        completed_list.append({
            'id': b.id,
            'name': b.name,
            'amount': float(b.amount),
            'spent': spent,
            'remaining': remaining,
            'used_percent': round(used_percent, 2),
            'start_date': b.start_date,
            'end_date': b.end_date,
            'completion_status': badge,
        })

    return render(request, "budget/budget_completed.html", {"budget_completed": completed_list})


# ==========================
# BUDGET ALERTS
# ==========================
def budget_alerts(request, budget):
    """
    Handles all alert logic for a single budget.
    Easy to extend — just add more conditions.
    """

    spent = budget.spent_amount()
    used_percent = budget.used_percent()

    # 1. Expired but still active
    if budget.is_expired() and budget.status == "active":
        messages.warning(
            request,
            f"Your budget '{budget.name}' expired on {budget.end_date}. "
            "You can still add expenses, but it is no longer active."
        )

    # 2. Overspent
    if used_percent > 100:
        messages.error(
            request,
            f"You have overspent the budget '{budget.name}'. "
            f"Current usage: {used_percent:.2f}%."
        )

    # 3. Near limit (90–100)
    elif used_percent >= 90:
        messages.warning(
            request,
            f"Your budget '{budget.name}' is close to the limit "
            f"({used_percent:.2f}% used)."
        )

    # Future examples:
    # if budget.remaining() < 100:
    #     messages.info(request, "Only ₹100 left in your budget.")

    return  # nothing to return — messages auto-save




