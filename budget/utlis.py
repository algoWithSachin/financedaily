from django.contrib import messages

def validate_budget_dates(request, start_date, end_date, budget_name="Budget"):
    """
    Validates start and end dates for a budget.
    Returns True if valid, False if invalid.
    """
    if start_date > end_date:
        messages.error(request, f"{budget_name}: Start date cannot be after end date.")
        return False
    return True


def validate_transaction_date(request, transaction_date, budget, transaction_name="Transaction"):
    """
    Validates that a transaction falls within the budget date range.
    Returns True if valid, False if invalid.
    """
    if transaction_date < budget.start_date or transaction_date > budget.end_date:
        messages.warning(
            request,
            f"{transaction_name} date ({transaction_date}) is outside the budget '{budget.name}' period "
            f"({budget.start_date} → {budget.end_date})."
        )
        return False
    return True


def validate_budget_amount(request, amount, budget_name="Budget"):
    """
    Optional: validate budget amount is positive.
    """
    if amount <= 0:
        messages.error(request, f"{budget_name}: Amount must be greater than zero.")
        return False
    return True
